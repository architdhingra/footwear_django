"""dApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views import View
import polls
from dApp import settings
from polls.views import *
from django.conf.urls.static import static
from dApp import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('signup/', signup, name="signup"),
    path('logout/', logout_view, name="logout_view"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),name="password_reset_complete"),
    path('about/', about, name="about"),
    path('profile/', profile_view, name="profile"),
    path(r'shop/<type>', shop, name="shop"),
    path('shopsingle/<slug>', ShopSingle.as_view(), name="shopsingle"),
    path('single/', single, name="single"),
    path('returns/', returns, name="returns"),
    path('blog/', blog, name="blog"),
    path('contact/', contact, name="contact"),
    path('login/', loginx, name="login"),
    path('test/', test, name="test"),
    # path('checkout/', checkout, name="checkout"),
    path('checkout/', Checkout.as_view(), name="checkout"),
    path('product/', product, name="product"),
    path('newlogin/', newLogin.as_view(), name="newLogin"),
    path('polls/', poll.as_view(), name="polls"),
    path('check/<id>', shopsingle, name="check"),
    path('delete/<id>', delete, name="delete"),
    path('addToCart/', addToCart, name="addToCart"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
