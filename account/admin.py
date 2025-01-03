from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات اضافی', {
            'fields': (
                'personnel_code',
                'department',
                'marital_status',
                'children_count',
                'hire_date',
                'employment_type',
            ),
        }),
    )

    list_display = (
        'username', 'first_name', 'last_name', 'email',
        'personnel_code', 'department', 'marital_status',
        'children_count', 'hire_date', 'employment_type'
    )

    list_filter = (
        'department', 'marital_status', 'employment_type',
    )

    search_fields = (
        'username', 'first_name', 'last_name', 'email', 'personnel_code'
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('اطلاعات اضافی', {
            'fields': (
                'personnel_code',
                'department',
                'marital_status',
                'children_count',
                'hire_date',
                'employment_type',
            ),
        }),
    )

admin.site.register(User, CustomUserAdmin)




