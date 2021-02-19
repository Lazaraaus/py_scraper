# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser 

# Create a Custom User Admin class
class CustomUserAdmin(UserAdmin):
    # Add Custom forms and Custom model 
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm 
    model = CustomUser 
    # List new fields on admin site
    list_display = ['email', 'username', 'position', 'searching', 'skills', 'is_staff',]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('position', 'searching', 'skills')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('position', 'searching', 'skills')}),
    )
# Register models on admin site 
admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.
