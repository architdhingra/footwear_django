from django.contrib import admin

# Register your models here.
from polls.models import Product


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # new


admin.site.register(Product, ProductAdmin)
