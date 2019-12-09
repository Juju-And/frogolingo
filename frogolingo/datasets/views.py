from django.shortcuts import render
from datasets.models import Expression, Translation
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.views.generic import FormView, UpdateView, CreateView, ListView
from datasets.forms import ExpressionForm, UploadFileForm
import speech_recognition as sr


# Create your views here.

class MainView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        return render(request, 'index.html', {})


class AddNewExpressionView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):

        # r = sr.Recognizer()
        # r.recognize_google()
        return render(request, 'add_expression.html', {})