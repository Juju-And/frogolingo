import json

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from datasets.models import Expression, UserStats, UserAnswer
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from datasets.forms import ExpressionForm


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
            return redirect('/all_expressions')

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
            status_color = "perfect"
        elif percentageAB > 30:
            status_color = "notbad"
        else:
            status_color = "critical"

        expressions_list.append({"expression": expressions[x],
                                 "percentage": percentageAB,
                                 "correct_answers": b,
                                 "all_answers": a,
                                 "status_color": status_color})
        expressions_list.sort(key=lambda x: x['percentage'])

        # if percentageAB <= percentage:
        # percentage = percentageAB
        # worst_expression = expressions[x]
    # print(worst_id)
    # print(percentage)
    # print(worst_expression)
    # print(random.choice(expressions_list[0:5]))

    return expressions_list


class StatsView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        expressions_list = selectWorstExpressions(user)
        expressions_list.sort(key=lambda x: x['percentage'], reverse=True)
        return render(request, 'stats.html', {'expressions_list': expressions_list})


class AllExpressionsView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        form = ExpressionForm()
        if request.GET.get('expression'):
            expression = request.GET.get('expression')
            # print(expression)
            expressions_list = Expression.objects.filter(user=user).filter(
                Q(translation__icontains=expression) |
                Q(reference__icontains=expression)).values()
        else:
            expressions_list = Expression.objects.filter(user=user)
        if request.GET.get('order_by'):
            order = request.GET.get('order_by')
            expressions_list = expressions_list.order_by(order)

        return render(request, 'all_expressions.html', {'expressions_list': expressions_list,
                                                        'form': form})

    def post(self, request):
        form = ExpressionForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
            return redirect('/all_expressions/')


class DeleteExpressionView(View):
    @csrf_exempt
    def delete(self, request, expression_id):
        try:
            expression = Expression.objects.get(id=expression_id)
            expression.delete()
            response = JsonResponse({'Message': 'Product deleted'}, safe=False)
        except ObjectDoesNotExist:
            response = JsonResponse({'Message': 'Invalid ID supplied'})
        return response


class EditExpressionView(LoginRequiredMixin, UpdateView):
    model = Expression
    fields = ['reference', 'translation', 'image', 'sound', ]
    template_name = 'edit_expression.html'
    success_url = '/all_expressions'
