from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="部門名稱")
    description = models.TextField(blank=True, null=True, verbose_name="部門描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = "部門"
        verbose_name_plural = "部門"

class JobTitle(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='職稱名稱')
    description = models.TextField(blank=True, null=True, verbose_name='職稱描述')
    level = models.PositiveSmallIntegerField(default=1, verbose_name='職級')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['level', 'name']
        verbose_name = '職稱'
        verbose_name_plural = '職稱'

class Employee(models.Model):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee', verbose_name='用戶')
    id_number = models.CharField(max_length=20, unique=True, verbose_name='身份證號碼', 
                                validators=[RegexValidator(regex=r'^[A-Z][12]\d{8}$', 
                                message='請輸入有效的身份證號碼')])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='性別')
    birth_date = models.DateField(null=True, blank=True, verbose_name='出生日期')
    photo = models.ImageField(upload_to='employee_photos', null=True, blank=True, verbose_name='照片')
    bio = models.TextField(blank=True, null=True, verbose_name='自傳')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='employees', verbose_name='部門')
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True, blank=True, 
                                 related_name='employees', verbose_name='職稱')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    
    def __str__(self):
        return f"{self.user.username} - {self.id_number}"
    
    class Meta:
        ordering = ['user__username']
        verbose_name = '員工'
        verbose_name_plural = '員工'
