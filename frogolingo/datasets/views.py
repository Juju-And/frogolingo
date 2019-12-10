from django.shortcuts import render, redirect
from datasets.models import Expression
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.views.generic import FormView, ListView
from datasets.forms import ExpressionForm
import speech_recognition as sr

from django.conf import settings
from django.core.files.storage import FileSystemStorage


# Create your views here.

class MainView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        # expressions = Expression.objects.all()
        expressions = Expression.objects.order_by('-id')[:10]
        # last_ten_in_ascending_order = reversed(expressions)
        return render(request, 'index.html', {'expressions': expressions})


# class AddNewExpressionView(LoginRequiredMixin, View):

# def post(self, request):
#     form = ExpressionForm(request.POST, request.FILES)
#     return render(request, 'add_expression.html', {'form': form})


class AddNewExpressionView(LoginRequiredMixin, View):
    def post(self, request):
        form = ExpressionForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
            return redirect('/')

    def get(self, request):
        form = ExpressionForm()
        return render(request, 'add_expression.html', {
            'form': form
        })


class AllExpressionView(ListView):
    pass


class AllAudioView(FormView):
    pass
#     template_name = "add_expression.html"
# form_class = ExpressionForm
# success_url = "/"
