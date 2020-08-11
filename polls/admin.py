from django.contrib import admin

# Register your models here.
from polls.models import *


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # new


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductColorImage)
admin.site.register(ProductSizeStock)
