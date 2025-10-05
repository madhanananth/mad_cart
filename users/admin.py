from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomerProfile, Address

class CustomerAdmin(UserAdmin):

    model = CustomerProfile
    list_display = ('id','email','is_staff','is_active','date_joined')
    list_filter = ('is_staff','is_active')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None,{'fields':('email','password')}),
        ('Permissions',{'fields':('is_staff','is_active','is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields': ('email', 'password1', 'password2'),

        }),
    )

admin.site.register(CustomerProfile,CustomerAdmin)
admin.site.register(Address)
