from django.shortcuts import render, redirect
from django.views.generic import FormView
from users.forms import LoginForm, CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, "User or password invalid!")
            return super().form_invalid(form)

    success_url = '/'


@login_required(login_url="/login")
def logoutUser(request):
    logout(request)
    return redirect("/")


class CreateUserView(FormView):
    template_name = "create_user.html"
    form_class = CreateUserForm
    success_url = "/"

    def form_valid(self, form):
        User.objects.create_user(
            username=form.cleaned_data['username'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )
        return super().form_valid(form)
