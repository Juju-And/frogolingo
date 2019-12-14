from django.shortcuts import render, redirect
from datasets.models import Expression, UserStats, UserAnswer
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
import json
import random

from datasets.views import selectWorstExpressions


class TrainingView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        expressions_list = selectWorstExpressions(user)
        random_word = (random.choice(expressions_list[0:5]))['expression']

        return render(request, 'training.html', {'random_word': random_word})

    def post(self, request):
        user = request.user
        # print(user.id)
        data = json.loads(request.body)
        expression_id = data['expression_id']
        # print(expression_id)
        answer = data['answer']
        UserAnswer.objects.create(
            user=user,
            expression_id=expression_id,
            is_correct=answer,
        )
        return redirect('/training')
        # return render(request, 'training.html', {})


class LearningView(View):
    def get(self, request):
        user = request.user
        expressions_list = selectWorstExpressions(user)
        random_word = (random.choice(expressions_list))['expression']

        return render(request, 'learning.html', {'random_word': random_word})


class NextExpressionsView(View):
    def get(self, request):
        user = request.user
        expressions_list = selectWorstExpressions(user)
        random_word = (random.choice(expressions_list))['expression']
        return render(request, 'next_expression_learn.html', {'random_word': random_word})
