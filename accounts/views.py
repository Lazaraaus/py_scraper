# accounts/views.py
from django.urls import reverse_lazy 
from django.views.generic import CreateView 

from .forms import CustomUserCreationForm
# Create SignUpView subclassing CreateView 
class SignUpView(CreateView):
    # Assign CustomUserCreationForm to our form class
    form_class = CustomUserCreationForm 
    # Assign success url to login
    success_url = reverse_lazy('login')
    # Assign a template to this view 
    template_name = 'registration/signup.html'

# Create your views here.
