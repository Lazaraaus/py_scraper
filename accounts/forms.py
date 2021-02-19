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
        # Set model and fields to our custom values 
        model = CustomUser
        fields = ('username',  'email', 'position', 'searching', 'skills')

# Custom admin change form class
class CustomUserChangeForm(UserChangeForm):
    # Meta class 
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'position', 'searching', 'skills')

