from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from djongo import models
from django.contrib.auth.models import User, auth


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
    slug = models.SlugField(max_length=40, default="", unique=True)
    discount = models.BigIntegerField(default=0)
    description = models.TextField(default="")

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
    color = models.CharField(default="", max_length=100)
    size = models.IntegerField(default=0)

    def getItems(self, userId):
        cart = Cart.objects.filter(user=userId)
        return cart

    def __str__(self):
        return self.product.name


class ProductSizeStock(models.Model):
    id = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
    size = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    sizeCm = models.IntegerField(default=0)

    def __str__(self):
        return self.pid.name


class ProductColorImage(models.Model):
    id = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
    color = models.CharField(default="", max_length=500)

    def __str__(self):
        return self.pid.name


class ProductImage(models.Model):
    product = models.ForeignKey(ProductColorImage, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/', default=None)

    def __str__(self):
        return self.product.pid.name


class Order(models.Model):
    status_choice = (
        ('Delivered', 'Delivered'),
        ('Out For Delivery', 'Out For Delivery'),
        ('In Progress', 'In Progress'),
    )
    orderStatusOptions = (
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid')
    )
    orderId = models.CharField(max_length=200, default="", primary_key=True)
    amount = models.FloatField(null=True)
    size = ArrayField(models.IntegerField(), null=True)
    color = ArrayField(models.CharField(max_length=500, default=""), null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=status_choice, default="In Progress")
    date = models.DateField(auto_now=True)
    orderStatus = models.CharField(max_length=100, choices=orderStatusOptions, default="Unpaid")

    # Order Address Fields
    address = models.CharField(max_length=50000, default="")
    number = models.CharField(default="0", max_length=20)
    name = models.CharField(max_length=500, default="")
    landmark = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=500, default="")
    country = models.CharField(max_length=500, default="India")
    postal_code = models.CharField(max_length=500, default="")

    # Tracking Fields
    courierPartner = models.CharField(max_length=1000, default="")
    trackingId = models.CharField(max_length=10000, default="")

    def __str__(self):
        return self.orderId


class OrderProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.order.orderId

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(default="", max_length=100)
    email = models.CharField(default="", max_length=100)
    phone = models.CharField(default="", max_length=100)
    message = models.CharField(default="", max_length=100000)

    def __str__(self):
        return self.name
