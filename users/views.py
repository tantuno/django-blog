from django.shortcuts import render
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from .models import CustomUser


class UserCreateView(CreateView):
    model = CustomUser
    template_name = 'users/signup.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        return render(self.request, 'users/registered.html')
