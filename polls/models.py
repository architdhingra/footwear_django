from django.contrib.auth.forms import UserCreationForm
from django.db import models

# Create your models here.
from django.views import View


class User(models.Model):
    uname = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

class newLogin(View):
    def get(self, *args, **kwargs):
        form = UserCreationForm()
        return form