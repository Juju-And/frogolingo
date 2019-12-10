from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Expression in foreign language
class Expression(models.Model):
    reference = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    image = models.FileField(upload_to='images/')
    sound = models.FileField(upload_to='sounds/')
    creation_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

