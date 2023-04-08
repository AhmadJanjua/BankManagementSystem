

from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy



def home_view(request):
    return render(request, 'home.html')

class LoginView(LoginView):
    template_name = 'login.html'

class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)