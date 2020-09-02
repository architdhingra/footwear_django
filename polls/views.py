from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.views import View
from django.views.generic import DetailView

from polls.forms import CreateUserForm
from polls.models import *
import requests
import json
import razorpay

client = razorpay.Client(auth=("rzp_test_oKQ9jz6Gyo5PdO", "yg3w0rMlvRA8OTUN8pLIKtF4"))


def index(request):
    prod = PopularProduct.objects.all()
    products = []
    images = []
    for j, product in enumerate(prod):
        products.append(product.product)
        p = ProductColorImage.objects.filter(pid=product.product)
        pi = ProductImage.objects.filter(product=p[0])
        images.append(pi[0].image.url)
    return render(request, "index.html", {'prod': products, 'images': images})


def signup(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        uname = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        storage = messages.get_messages(request)
        storage.used = True
        if password2 == password:
            if User.objects.filter(username=uname).exists():
                messages.info(request, "User Already Exists!")
                return render(request, "signup.html")
            else:
                user = User.objects.create_user(first_name=fname, last_name=lname, username=uname, password=password,
                                                email=uname)
                user.save()
                messages.info(request, "Registered Successfully!")
                return render(request, "login.html",)
        return render(request, 'signup.html')

    else:
        return render(request, "signup.html")


def loginx(request):
    if request.method == "POST":
        uname = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(username=uname, password=password)
        storage = messages.get_messages(request)
        storage.used = True
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, "Invalid Credentials!")
            return render(request, "login.html")

    else:
        return render(request, "login.html")


def logout_view(request):
    Product.logout_model(request)
    return render(request, "login.html")


class newLogin(View):
    def get(self, *args, **kwargs):
        form = CreateUserForm()
        return render(self.request, "newLogin.html", {'form': form})

    def post(self, *args, **kwargs):
        form = CreateUserForm(self.request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(self.request, "newLogin.html", {'form': form})


def password_reset(request):
    return render(request, 'password_reset.html')


def password_reset_done(request):
    return render(request, 'password_reset_done.html')


def about(request):
    return render(request, "index.html", {})


def shop(request, type):
    prod = Product.getProducts(request, type)
    images = []
    for j, product in enumerate(prod):
        p = ProductColorImage.objects.filter(pid=product)
        pi = ProductImage.objects.filter(product=p[0])
        images.append(pi[0].image.url)
    return render(request, "shop.html", {'prod': prod, 'images': images})


def returns(request):
    return render(request, "returns.html", {})


class ShopSingle(DetailView):
    model = Product
    template_name = 'shopsingle.html'
    Product.objects.all().update(discount=F('origPrice') - F('price'))

    def get_context_data(self, *args, **kwargs):
        context = super(ShopSingle, self).get_context_data(**kwargs)
        p = ProductColorImage.objects.filter(pid=self.object)
        pi = ProductImage.objects.filter(product=p[0])
        ps = ProductSizeStock.objects.filter(pid=self.object)
        context["images"] = pi
        context["color"] = p
        context["sizes"] = ps
        return context

    def post(self, request, slug, *args, **kwargs):
        self.object = self.get_object()
        context = super(ShopSingle, self).get_context_data(**kwargs)
        context["color"] = ProductColorImage.objects.filter(pid=self.object)
        ps = ProductSizeStock.objects.filter(pid=self.object)
        p = ProductColorImage.objects.filter(pid=self.object, color=self.request.POST['color'])
        pi = ProductImage.objects.filter(product=p[0])
        context["images"] = pi
        context["sizes"] = ps
        return self.render_to_response(context=context)


class Checkout(View):

    def post(self, *args, **kwargs):
        pid = (self.request.POST['pid'])
        size = (self.request.POST['size'])
        color = (self.request.POST['color'])
        c = Cart.objects.create(user=self.request.user, product=Product.getSingle(self.request, id=pid),
                                color=color,
                                size=size)
        try:
            c.save()
        except:
            return HttpResponse(400)

        items = Cart.getItems(self.request, self.request.user)
        totalPrice = 0
        images = []
        for item in items:
            totalPrice += item.product.price
            p = ProductColorImage.objects.filter(pid=item.product, color=item.color)
            pi = ProductImage.objects.filter(product=p[0])
            images.append(pi[0])
        return render(self.request, "checkout.html", {'items': items, 'totalPrice': totalPrice, 'images': images})

    def get(self, *args, **kwargs):
        images = []
        items = Cart.getItems(self.request, self.request.user)
        totalPrice = 0
        for item in items:
            totalPrice += item.product.price
            p = ProductColorImage.objects.filter(pid=item.product, color=item.color)
            pi = ProductImage.objects.filter(product=p[0])
            images.append(pi[0])
        return render(self.request, "checkout.html", {'items': items, 'totalPrice': totalPrice, 'images': images})


def blog(request):
    return render(request, "blog.html", {})


def test(request):
    URL = 'https://checkout.razorpay.com/v1/checkout.js'

    return render(request, "test.html", {})


def product(request):
    return render(request, "product.html", {})


def check(request):
    return render(request, "check.html", {})


def delete(request, id):
    Cart.objects.filter(id=id).delete()
    print("deleted")
    return HttpResponse(200)


def addToCart(request):
    pid = (request.POST['pid'])
    size = (request.POST['size'])
    color = (request.POST['color'])
    c = Cart.objects.create(user=request.user, product=Product.getSingle(request, id=pid), color=color,
                            size=size)
    try:
        c.save()
        return HttpResponse(200)
    except:
        return HttpResponse(400)


def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email1 = request.POST["email"]
        phone = request.POST["phone"]
        message = request.POST["message"]
        message = Contact.objects.create(name=name, email=email1, phone=phone, message=message)
        message.save()
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request, "Your Query has been successfully submitted! We will connect with you shortly")
        return render(request, 'contact.html')

    else:
        return render(request, "contact.html")


def profile_view(request):
    if request.method == "GET":
        orders = Order.objects.filter(user=request.user, orderStatus='Paid')
        prods = []
        products = {}
        images = []
        img = {}
        for i, order in enumerate(orders):
            pz = OrderProducts.objects.filter(order=order)

            for j, productz in enumerate(pz):
                prods.append(productz.product)
                color = order.color[j]
                p = ProductColorImage.objects.filter(pid=productz.product, color=color)
                pi = ProductImage.objects.filter(product=p[0])
                images.append(pi[0].image.url)
            img[i] = images
            products[i] = prods
            prods = []
            images = []
        print(products)
        return render(request, 'profile.html', {'results': orders, 'products': products, 'images': img})


def payment_confirmation(request):
    context = {}

    items = Cart.getItems(request, request.user)
    totalPrice = 0
    products, size, color = [], [], []
    for item in items:
        totalPrice += item.product.price
        products.append(item.product)
        size.append(item.size)
        color.append(item.color)

    order_currency = 'INR'
    notes = {
        'Shipping address': request.POST['address']}
    # CREATING ORDER
    response = client.order.create(
        dict(amount=totalPrice * 100, currency=order_currency, notes=notes, payment_capture='0'))

    o = Order.objects.create(orderId=response['id'], amount=totalPrice, size=size, color=color,
                             user=request.user,
                             address=request.POST['address'], name=request.POST['name'], number=request.POST['number'],
                             landmark=request.POST['landmark'], city=request.POST['city'], country='India',
                             postal_code=request.POST['postal'])
    for p in products:
        op = OrderProducts.objects.create(order_id=o.orderId, product=p)
        op.save()
    o.save()
    order_id = response['id']
    order_status = response['status']

    if order_status == 'created':
        context['product_id'] = order_id
        context['price'] = totalPrice
        context['name'] = request.user.first_name
        context['phone'] = o.number
        context['email'] = request.user.email

        # data that'll be send to the razorpay for
        context['order_id'] = order_id
        context['order_date'] = o.date
        context['address'] = o.address
        context['city'] = o.city
        context['totalPrice'] = totalPrice
        context['country'] = o.country
        context['postal'] = o.postal_code

        print('created order')
        return render(request, 'payment_confirmation.html', context)

    return HttpResponse('<h1>Error in  create order function</h1>')


def payment_status(request):
    response = request.POST
    print(response)
    o = Order.objects.get(orderId=response['razorpay_order_id'])
    print(o)

    params_dict = {
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_signature': response['razorpay_signature']
    }
    # VERIFYING SIGNATURE
    try:
        status = client.utility.verify_payment_signature(params_dict)
        o.orderStatus = 'Paid'
        o.save()
        return render(request, 'payment.html', {'status': 'Successful', 'payment_id': response['razorpay_order_id']})
    except:
        return render(request, 'payment.html',
                      {'status': 'UnSuccessful', 'payment_id': response['razorpay_payment_id']})
