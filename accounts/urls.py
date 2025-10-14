from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('permissions/', views.permissions_panel, name='permissions_panel'),
    path('user-permissions/<int:user_id>/', views.user_permissions, name='user_permissions'),
    path('groups/', views.group_list, name='group_list'),
    path('groups/create/', views.group_create, name='group_create'),
    path('groups/<int:group_id>/edit/', views.group_edit, name='group_edit'),
    path('groups/<int:group_id>/delete/', views.group_delete, name='group_delete'),
    path('groups/<int:group_id>/permissions/', views.group_permissions, name='group_permissions'),
    path('groups/<int:group_id>/members/', views.group_members, name='group_members'),
    # 部門管理路由
    path('departments/', views.department_list, name='department_list'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/<int:department_id>/edit/', views.department_edit, name='department_edit'),
    path('departments/<int:department_id>/delete/', views.department_delete, name='department_delete'),
    # 職稱管理路由
    path('jobtitles/', views.jobtitle_list, name='jobtitle_list'),
    path('jobtitles/create/', views.jobtitle_create, name='jobtitle_create'),
    path('jobtitles/<int:jobtitle_id>/edit/', views.jobtitle_edit, name='jobtitle_edit'),
    path('jobtitles/<int:jobtitle_id>/delete/', views.jobtitle_delete, name='jobtitle_delete'),
    # 員工管理路由
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<int:employee_id>/edit/', views.employee_edit, name='employee_edit'),
    path('employees/<int:employee_id>/delete/', views.employee_delete, name='employee_delete'),
]