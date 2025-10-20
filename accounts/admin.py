from django.contrib import admin
    # admin.py
from django_summernote.admin import SummernoteModelAdmin
from .models import Employee

class PostAdmin(SummernoteModelAdmin):
        summernote_fields = '__all__' # 'content' is the field in your Post model

admin.site.register(Employee, PostAdmin)
# Register your models here.
