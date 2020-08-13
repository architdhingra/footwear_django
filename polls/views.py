from datetime import datetime
from django import template
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
# Create your views here.
from django.template import context
from django.views import View
from django.views.generic import DetailView
from polls.forms import CreateUserForm
from polls.models import NewLogin, Product, Cart, ProductColorImage, ProductImage, Contact, Order


def index(request):
    ing = NewLogin.index(request)
    return render(request, "index.html", ing)


def signup(request):
    if request.method == "POST":
        fname= request.POST["fname"]
        lname = request.POST["lname"]
        uname = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        contexts = {"aa": uname, "bb": password}
        if password2 == password:
            if User.objects.filter(username=uname).exists():
                messages.info(request, "already exists")
                return redirect('signup')
            else:
                user = User.objects.create_user(first_name=fname,last_name=lname, username=uname, password=password)
                user.save()
                messages.info(request, "Registered Successfully!")
                return redirect('polls')
        return render(request, 'signup.html', contexts)

    else:
        today = datetime.now().date()
        contexts = {"aa": 11, "bb": 22}
        return render(request, "signup.html")


def loginx(request):
    if request.method == "POST":
        uname = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(username=uname, password=password)

        if user is not None:
            login(request, user)
            return redirect('polls')
        else:
            return render(request, "login.html")

    else:
        return render(request, "login.html")


def logout_view(request):
    Product.logout_model(request)
    return render(request, "login.html")


class poll(View):
    def get(self, *args, **kwargs):
        return render(self.request, "index.html", {})



class newLogin(View):
    def get(self, *args, **kwargs):
        form = CreateUserForm()
        return render(self.request, "newLogin.html", {'form': form})

    def post(self, *args, **kwargs):
        form = CreateUserForm(self.request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls')
        return render(self.request, "newLogin.html", {'form': form})


def password_reset(request):
    return render(request, 'password_reset.html')


def password_reset_done(request):
    return render(request, 'password_reset_done.html')


def password_reset_confirm(request):
    return render(request, 'password_reset_confirm.html')


def about(request):
    return render(request, "about.html", {})


@login_required()
def shop(request, type):
    prod = Product.getProducts(request, type)
    return render(request, "shop.html", {'prod': prod})


def shopsingle(request, id):
    prod = Product.getSingle(request, id)
    return render(request, "check.html", {'prod': prod})


def returns(request):
    return render(request, "returns.html", {})


class ShopSingle(DetailView):
    model = Product
    template_name = 'shopsingle.html'
    Product.objects.all().update(discount=F('origPrice') - F('price'))

    def get_context_data(self, *args, **kwargs):
        context = super(ShopSingle, self).get_context_data(**kwargs)
        context["color"] = ProductColorImage.objects.filter(pid=self.object)
        p = ProductColorImage.objects.filter(pid=self.object)
        print(p[0].color)
        pi = ProductImage.objects.filter(product=p[0])
        print(pi[0].image.url)
        context["images"] = pi

        return context


class Checkout(View):
    def post(self, *args, **kwargs):
        pid = (self.request.POST['pid'])
        size = (self.request.POST['size'])
        color = (self.request.POST['color'])
        c = Cart.objects.create(user=self.request.user, product=Product.getSingle(self.request, id=pid), quantity=1,
                                color=color,
                                size=size)
        try:
            c.save()
        except:
            return HttpResponse(400)

        items = Cart.getItems(self.request, self.request.user)
        totalPrice = 0
        for item in items:
            totalPrice += item.product.price
        print(totalPrice)
        return render(self.request, "checkout.html", {'items': items, 'totalPrice': totalPrice})

    def get(self, *args, **kwargs):
        items = Cart.getItems(self.request, self.request.user)
        print(items)
        totalPrice = 0
        for item in items:
            totalPrice += item.product.price
        print(totalPrice)
        return render(self.request, "checkout.html", {'items': items, 'totalPrice': totalPrice})


def single(request):
    
    return render(request, "single.html", {})


def blog(request):
    return render(request, "blog.html", {})




def test(request):
    return render(request, "test.html", {})


def product(request):
    return render(request, "product.html", {})


def checkout1(request):
    return render(request, "checkout.html", {})


def checkout(request, id):
    cd = Cart.objects.filter(user=request.user, product=Product.getSingle(request, id=id))
    items = Cart.getItems(request, request.user)
    print(items)
    return render(request, "checkout.html", {'items': items})


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
    c = Cart.objects.create(user=request.user, product=Product.getSingle(request, id=pid), quantity=1, color=color,
                            size=size)
    try:
        c.save()
        return HttpResponse(200)
    except:
        return HttpResponse(400)

def contact(request):
    if request.method == "POST":
        name= request.POST["name"]
        email1 = request.POST["email"]
        phone = request.POST["phone"]
        message = request.POST["message"]
        message = Contact.objects.create(name=name,email=email1, phone=phone, message=message)
        message.save()
        messages.info(request, "Your Query has been successfully submitted! We will connect with you shortly")
        return redirect('polls')

    else:
        today = datetime.now().date()
        return render(request, "contact.html")

def profile_view(request):
    if request.method == "GET":
        results = Order.objects.filter(user=request.user)
        print (results)
        return render(request, 'profile.html', {'results':results})
