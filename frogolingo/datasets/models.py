from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Expression in foreign language
class Expression(models.Model):
    content = models.CharField(max_length=100)
    image = models.CharField(max_length=256)
    sound = models.FileField(max_length=256)
    creation_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# Translation of the foreign expression
class Translation(models.Model):
    content = models.CharField(max_length=100)
    reference = models.OneToOneField(Expression, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
