from django.shortcuts import render
from datasets.models import Expression, Translation
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.views.generic import FormView, UpdateView, CreateView, ListView
from datasets.forms import ExpressionForm


# Create your views here.

class MainView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        return render(request, 'index.html', {})


class AddNewExpressionView(LoginRequiredMixin, CreateView):
    login_url = '/login'

    template_name = "add_expression.html"
    form_class = ExpressionForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
