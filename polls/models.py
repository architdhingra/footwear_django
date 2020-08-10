from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from djongo import models
from django.contrib.auth.models import User,auth


# class User(models.Model):
#     uname = models.CharField(max_length=200)
#     password = models.CharField(max_length=200)


class NewLogin(models.Model):
    def get(self, *args, **kwargs):
        form = UserCreationForm()
        return form

    def index(self):
        contexts = {"aa": 11, "bb": 22}
        return contexts


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=5000, default="")
    origPrice = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    type = models.CharField(max_length=500, default="")
    material = models.CharField(max_length=50000, default="")
    details = models.CharField(max_length=50000, default="")
    color = models.CharField(max_length=100, default="")
    slug = models.SlugField(max_length=40, default="", unique=True)
    discount = models.BigIntegerField(default=0)


    class Meta:
        db_table = "Product"

    def getProducts(self, type):
        prod = Product.objects.filter(type=type)
        return prod

    def getSingle(self, id):
        prod = Product.objects.get(id=id)
        return prod

    def __str__(self):
        return self.name

    def logout_model(self):
        auth.logout(self)


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
    quantity = models.IntegerField(default=1)
    color = models.CharField(default="", max_length=100)
    size = models.IntegerField(default=0)

    def getItems(self, userId):
        cart = Cart.objects.filter(user=userId)
        return cart


class ProductSizeStock(models.Model):
    id = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
    size = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    sizeCm = models.IntegerField(default=0)

    def __str__(self):
        return self.pid.name


class ProductColorImages(models.Model):
    id = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
    color = models.CharField(default="", max_length=500)
    pics = ArrayField(models.CharField(max_length=10000), null=True, blank=True)

    def __str__(self):
        return self.pid.name