from django.db import models
from django.contrib.auth.models import User


class Expression(models.Model):
    reference = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    image = models.FileField(upload_to='images/')
    sound = models.FileField(upload_to='sounds/')
    creation_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class UserAnswer(models.Model):
    expression = models.ForeignKey(Expression, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)


class UserStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct_answers_reference_counter = models.IntegerField(default=0)
    wrong_answers_reference_counter = models.IntegerField(default=0)
    correct_answers_translation_counter = models.IntegerField(default=0)
    wrong_answers_translation_counter = models.IntegerField(default=0)
