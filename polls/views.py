from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.template import context
from django.views import View

from polls.forms import CreateUserForm
from polls.models import NewLogin, Product


def index(request):
    ing = NewLogin.index(request)
    return render(request, "index.html", ing)


def signup(request):
    if request.method == "POST":
        uname = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        messages.info(request, "Registered Successfully!")
        contexts = {"aa": uname, "bb": password}
        if password2 == password:
            if User.objects.filter(username=uname).exists():
                messages.info(request, "already exists")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=uname, password=password)
                user.save()
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


def about(request):
    return render(request, "about.html", {})


def shop(request, type):
    prod = Product.getProducts(request, type)
    return render(request, "shop.html", {'prod': prod})


def shopsingle(request, id):
    prod = Product.getSingle(request, id)
    return render(request, "shopsingle.html", {'prod': prod})

def shopsingle1(request):
    return render(request, "shopsingle.html", {})

def single(request):
    return render(request, "single.html", {})


def blog(request):
    return render(request, "blog.html", {})


def contact(request):
    return render(request, "contact.html", {})


def test(request):
    prod = Product.getSingle(request, 2)
    print(prod.pics)
    return render(request, "test.html", {'prod': prod})


def product(request):
    return render(request, "product.html", {})


def checkout(request):
    return render(request, "checkout.html", {})
