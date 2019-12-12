from django.shortcuts import render, redirect
from datasets.models import Expression, UserStats, UserAnswer
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.views.generic import ListView
from datasets.forms import ExpressionForm
import speech_recognition as sr
import json


class MainView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        expressions = Expression.objects.order_by('-id')[:10]
        return render(request, 'index.html', {'expressions': expressions})


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


class MessagesView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'messages.html', {})


class StatsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'stats.html', {})


class TrainingView(LoginRequiredMixin, View):
    def get(self, request):
        random_word = Expression.objects.order_by('?').first()
        return render(request, 'training.html', {'random_word': random_word})

    def post(self, request):
        user = request.user
        print(user.id)
        data = json.loads(request.body)
        expression_id = data['expression_id']
        answer = data['answer']
        UserAnswer.objects.create(
            user=user,
            expression_id=expression_id,
            is_correct=answer,
        )

        return render(request, 'training.html', {})


class AllExpressionView(LoginRequiredMixin, View):
    pass
