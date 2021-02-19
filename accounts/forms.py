# accounts/forms.py
# Handling CustomUser model within Django admin app

# Imports 
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from .models import CustomUser

# Create Custom admin user creation form class
class CustomUserCreationForm(UserCreationForm):
    # Create a Meta class
    class Meta(UserCreationForm):
        # Override the default model (and fields) 
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('position', 'searching', 'skills')

# Custom admin change form class
class CustomUserChangeForm(UserChangeForm):
    # Meta class 
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields 

