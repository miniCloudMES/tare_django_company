from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from .forms import CustomUserCreationForm
from .models import Department, JobTitle, Employee

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# Check if user is admin
def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(is_admin)
def permissions_panel(request):
    users = User.objects.all().order_by('username')
    groups = Group.objects.all().order_by('name')
    content_types = ContentType.objects.all().order_by('app_label', 'model')
    permissions = Permission.objects.all().order_by('content_type__app_label', 'codename')
    
    context = {
        'users': users,
        'groups': groups,
        'content_types': content_types,
        'permissions': permissions,
    }
    
    return render(request, 'accounts/permissions_panel.html', context)

@login_required
@user_passes_test(is_admin)
def group_list(request):
    groups = Group.objects.all().order_by('name')
    return render(request, 'accounts/group_list.html', {'groups': groups})

@login_required
@user_passes_test(is_admin)
def group_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            group = Group.objects.create(name=name)
            messages.success(request, f'Group "{name}" created successfully')
            return redirect('group_permissions', group_id=group.id)
        else:
            messages.error(request, 'Group name is required')
    return render(request, 'accounts/group_form.html')

@login_required
@user_passes_test(is_admin)
def group_edit(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            group.name = name
            group.save()
            messages.success(request, f'Group renamed to "{name}" successfully')
            return redirect('group_list')
        else:
            messages.error(request, 'Group name is required')
    return render(request, 'accounts/group_form.html', {'group': group})

@login_required
@user_passes_test(is_admin)
def group_delete(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        name = group.name
        group.delete()
        messages.success(request, f'Group "{name}" deleted successfully')
        return redirect('group_list')
    return render(request, 'accounts/group_confirm_delete.html', {'group': group})

@login_required
@user_passes_test(is_admin)
def group_permissions(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group_permissions = group.permissions.all()
    all_permissions = Permission.objects.all().order_by('content_type__app_label', 'codename')
    
    if request.method == 'POST':
        # Clear existing permissions
        group.permissions.clear()
        
        # Add selected permissions
        permission_ids = request.POST.getlist('permissions')
        for permission_id in permission_ids:
            permission = Permission.objects.get(id=permission_id)
            group.permissions.add(permission)
        
        messages.success(request, f'Permissions updated for group "{group.name}"')
        return redirect('group_list')
    
    context = {
        'group': group,
        'group_permissions': group_permissions,
        'all_permissions': all_permissions,
    }
    
    return render(request, 'accounts/group_permissions.html', context)

@login_required
@user_passes_test(is_admin)
def group_members(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group_members = User.objects.filter(groups=group).order_by('username')
    all_users = User.objects.all().order_by('username')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        user_ids = request.POST.getlist('users')
        
        if action == 'add':
            for user_id in user_ids:
                user = User.objects.get(id=user_id)
                user.groups.add(group)
            messages.success(request, f'Users added to group "{group.name}" successfully')
        
        elif action == 'remove':
            for user_id in user_ids:
                user = User.objects.get(id=user_id)
                user.groups.remove(group)
            messages.success(request, f'Users removed from group "{group.name}" successfully')
        
        return redirect('group_members', group_id=group.id)
    
    context = {
        'group': group,
        'group_members': group_members,
        'all_users': all_users,
    }
    
    return render(request, 'accounts/group_members.html', context)

# 部門管理視圖
@login_required
@user_passes_test(is_admin)
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'accounts/department_list.html', {'departments': departments})

@login_required
@user_passes_test(is_admin)
def department_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            department = Department.objects.create(name=name, description=description)
            messages.success(request, f'部門 "{name}" 創建成功')
            return redirect('department_list')
        else:
            messages.error(request, '部門名稱不能為空')
    return render(request, 'accounts/department_form.html')

@login_required
@user_passes_test(is_admin)
def department_edit(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            department.name = name
            department.description = description
            department.save()
            messages.success(request, f'部門 "{name}" 更新成功')
            return redirect('department_list')
        else:
            messages.error(request, '部門名稱不能為空')
    return render(request, 'accounts/department_form.html', {'department': department})

@login_required
@user_passes_test(is_admin)
def department_delete(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        name = department.name
        department.delete()
        messages.success(request, f'部門 "{name}" 刪除成功')
        return redirect('department_list')
    return render(request, 'accounts/department_confirm_delete.html', {'department': department})

# 職稱管理視圖
@login_required
@user_passes_test(is_admin)
def jobtitle_list(request):
    jobtitles = JobTitle.objects.all()
    return render(request, 'accounts/jobtitle_list.html', {'jobtitles': jobtitles})

@login_required
@user_passes_test(is_admin)
def jobtitle_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        level = request.POST.get('level', 1)
        if name:
            jobtitle = JobTitle.objects.create(name=name, description=description, level=level)
            messages.success(request, f'職稱 "{name}" 創建成功')
            return redirect('jobtitle_list')
        else:
            messages.error(request, '職稱名稱不能為空')
    return render(request, 'accounts/jobtitle_form.html')

@login_required
@user_passes_test(is_admin)
def jobtitle_edit(request, jobtitle_id):
    jobtitle = get_object_or_404(JobTitle, id=jobtitle_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        level = request.POST.get('level', 1)
        if name:
            jobtitle.name = name
            jobtitle.description = description
            jobtitle.level = level
            jobtitle.save()
            messages.success(request, f'職稱 "{name}" 更新成功')
            return redirect('jobtitle_list')
        else:
            messages.error(request, '職稱名稱不能為空')
    return render(request, 'accounts/jobtitle_form.html', {'jobtitle': jobtitle})

@login_required
@user_passes_test(is_admin)
def jobtitle_delete(request, jobtitle_id):
    jobtitle = get_object_or_404(JobTitle, id=jobtitle_id)
    
    if request.method == 'POST':
        jobtitle.delete()
        messages.success(request, f'職稱 "{jobtitle.name}" 已成功刪除')
        return redirect('jobtitle_list')
    
    return render(request, 'accounts/jobtitle_confirm_delete.html', {'jobtitle': jobtitle})

# 員工管理視圖
@login_required
@user_passes_test(is_admin)
def employee_list(request):
    employees = Employee.objects.all().select_related('user', 'department', 'job_title')
    return render(request, 'accounts/employee_list.html', {'employees': employees})

@login_required
@user_passes_test(is_admin)
def employee_create(request):
    if request.method == 'POST':
        # 獲取表單數據
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        id_number = request.POST.get('id_number')
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date') or None
        bio = request.POST.get('bio')
        department_id = request.POST.get('department')
        job_title_id = request.POST.get('job_title')
        
        # 檢查用戶名是否已存在
        if User.objects.filter(username=username).exists():
            messages.error(request, f'用戶名 "{username}" 已存在，請使用其他用戶名')
            departments = Department.objects.all()
            job_titles = JobTitle.objects.all()
            return render(request, 'accounts/employee_form.html', {
                'departments': departments,
                'job_titles': job_titles,
                'form_data': request.POST,  # 保留表單數據以便用戶修改
                'error': '用戶名已存在'
            })
        
        try:
            with transaction.atomic():
                # 創建用戶
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # 創建員工資料
                employee = Employee.objects.create(
                    user=user,
                    id_number=id_number,
                    gender=gender,
                    birth_date=birth_date,
                    bio=bio
                )
                
                # 處理照片上傳
                if 'photo' in request.FILES:
                    employee.photo = request.FILES['photo']
                
                # 關聯部門和職稱
                if department_id:
                    employee.department_id = department_id
                if job_title_id:
                    employee.job_title_id = job_title_id
                
                employee.save()
                
                messages.success(request, f'員工 "{username}" 已成功創建')
                return redirect('employee_list')
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e) and 'username' in str(e):
                messages.error(request, f'用戶名 "{username}" 已存在，請使用其他用戶名')
            elif 'UNIQUE constraint' in str(e) and 'id_number' in str(e):
                messages.error(request, f'身份證號 "{id_number}" 已存在，請檢查輸入')
            else:
                messages.error(request, f'創建員工時出錯: {str(e)}')
        except Exception as e:
            messages.error(request, f'創建員工時出錯: {str(e)}')
    
    # 獲取部門和職稱列表
    departments = Department.objects.all()
    job_titles = JobTitle.objects.all()
    
    return render(request, 'accounts/employee_form.html', {
        'departments': departments,
        'job_titles': job_titles
    })

@login_required
@user_passes_test(is_admin)
def employee_edit(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        # 獲取表單數據
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        id_number = request.POST.get('id_number')
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date') or None
        bio = request.POST.get('bio')
        department_id = request.POST.get('department')
        job_title_id = request.POST.get('job_title')
        
        try:
            with transaction.atomic():
                # 更新用戶資料
                user = employee.user
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                
                # 更新員工資料
                employee.id_number = id_number
                employee.gender = gender
                employee.birth_date = birth_date
                employee.bio = bio
                
                # 處理照片上傳
                if 'photo' in request.FILES:
                    employee.photo = request.FILES['photo']
                
                # 關聯部門和職稱
                employee.department_id = department_id if department_id else None
                employee.job_title_id = job_title_id if job_title_id else None
                
                employee.save()
                
                messages.success(request, f'員工 "{user.username}" 資料已成功更新')
                return redirect('employee_list')
        except Exception as e:
            messages.error(request, f'更新員工資料時出錯: {str(e)}')
    
    # 獲取部門和職稱列表
    departments = Department.objects.all()
    job_titles = JobTitle.objects.all()
    
    return render(request, 'accounts/employee_form.html', {
        'employee': employee,
        'departments': departments,
        'job_titles': job_titles
    })

@login_required
@user_passes_test(is_admin)
def employee_delete(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        username = employee.user.username
        
        # 刪除用戶會級聯刪除員工記錄
        employee.user.delete()
        
        messages.success(request, f'員工 "{username}" 已成功刪除')
        return redirect('employee_list')
    
    return render(request, 'accounts/employee_confirm_delete.html', {'employee': employee})

@login_required
@user_passes_test(is_admin)
def user_permissions(request, user_id):
    user = User.objects.get(id=user_id)
    user_permissions = user.user_permissions.all()
    all_permissions = Permission.objects.all().order_by('content_type__app_label', 'codename')
    user_groups = user.groups.all()
    all_groups = Group.objects.all().order_by('name')
    
    if request.method == 'POST':
        # Clear existing permissions
        user.user_permissions.clear()
        
        # Add selected permissions
        permission_ids = request.POST.getlist('permissions')
        for permission_id in permission_ids:
            permission = Permission.objects.get(id=permission_id)
            user.user_permissions.add(permission)
        
        # Update staff status
        if 'is_staff' in request.POST:
            user.is_staff = True
        else:
            user.is_staff = False
            
        # Update superuser status
        if 'is_superuser' in request.POST:
            user.is_superuser = True
        else:
            user.is_superuser = False
        
        # Update group membership
        user.groups.clear()
        group_ids = request.POST.getlist('groups')
        for group_id in group_ids:
            group = Group.objects.get(id=group_id)
            user.groups.add(group)
            
        user.save()
        messages.success(request, f'Permissions updated for {user.username}')
        return redirect('permissions_panel')
    
    context = {
        'user_obj': user,
        'user_permissions': user_permissions,
        'all_permissions': all_permissions,
        'user_groups': user_groups,
        'all_groups': all_groups,
    }
    
    return render(request, 'accounts/user_permissions.html', context)