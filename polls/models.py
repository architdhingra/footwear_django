from django.contrib.auth.forms import UserCreationForm
from django.contrib.postgres.fields import ArrayField
from django.db import models
from djongo import models



class User(models.Model):
    uname = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


class NewLogin(models.Model):
    def get(self, *args, **kwargs):
        form = UserCreationForm()
        return form

    def index(self):
        contexts = {"aa": 11, "bb": 22}
        return contexts

class Cart(models.Model):
    def addProduct(self):
        return


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=5000, default="")
    origPrice = models.BigIntegerField(default=0)
    price = models.BigIntegerField(default=0)
    size = models.IntegerField(default=0)
    sizeCm = models.BigIntegerField(default=0)
    type = models.CharField(max_length=500, default="")
    material = models.CharField(max_length=50000, default="")
    stock = models.BigIntegerField(default=0)
    availabilty = models.BooleanField(default=True)
    details = models.CharField(max_length=50000, default="")
    color = models.CharField(max_length=100, default="")
    pics = ArrayField(models.CharField(max_length=10000), null=True, blank=True)

    class Meta:
        db_table = "Product"

    def getProducts(self, type):
        prod = Product.objects.filter(type=type)
        return prod

    def getSingle(self, id):
        prod = Product.objects.get(id=id)
        return prod