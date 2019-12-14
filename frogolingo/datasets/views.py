from multiprocessing.reduction import register

from django.shortcuts import render, redirect
from datasets.models import Expression, UserStats, UserAnswer
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.views.generic import ListView
from datasets.forms import ExpressionForm
import speech_recognition as sr
import json
import random


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


# user_answers
#
# expresion_id
# is_correct
# user_id
#
# 1, true, 1
# 1, true, 1
# 1, false, 1
# 1, false, 1
# 1, false, 1
# 2, true, 1
# 2, true, 1
# 2, false, 1
# 1, false, 2
# 2, true, 2
# 2, true, 2
# 2, false, 2
#
#
# a = select count(*) from user_answers where user_id = 1 and expression_id = 1
# b = select count(*) from user_answers where user_id = 1 and expression_id = 1 and is_correct = true
#
# b / a * 100

def selectWorstExpressions(user):
    expressions = Expression.objects.all()
    percentage = 100.0
    # worst_expression = expressions[0]
    expressions_list = []
    for x in range(0, len(expressions)):
        # Returns the total number of entries in the database.
        a = UserAnswer.objects.filter(user=user).filter(expression_id=expressions[x].id).count()
        # Returns the number of entries whose answer were correct
        b = UserAnswer.objects.filter(user=user).filter(expression_id=expressions[x].id).filter(
            is_correct=True).count()
        if a != 0 and b != 0:
            percentageAB = round(b / a * 100, 2)
        else:
            percentageAB = 0.0
        print("a =", a, "b =", b, "procent =", percentageAB)

        if percentageAB > 90:
            color = "perfect"
        elif percentageAB > 50:
            color = "notbad"
        else:
            color = "critical"

        expressions_list.append({"expression": expressions[x],
                                 "percentage": percentageAB,
                                 "correct_answers": b,
                                 "all_answers": a,
                                 "status_color": color})
        expressions_list.sort(key=lambda x: x['percentage'])

        # if percentageAB <= percentage:
        # percentage = percentageAB
        # worst_expression = expressions[x]
    # print(worst_id)
    # print(percentage)
    # print(worst_expression)
    # print(random.choice(expressions_list[0:5]))

    return expressions_list


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


class StatsView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        expressions_list = selectWorstExpressions(user)
        expressions_list.sort(key=lambda x: x['percentage'], reverse=True)
        return render(request, 'stats.html', {'expressions_list': expressions_list})


class AllExpressionsView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        expressions_list = Expression.objects.filter(user=user)
        return render(request, 'all_espressions.html', {'expressions_list': expressions_list})
