from django.contrib import admin

# Register your models here.
from polls.models import *


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # new


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    extra = 1


@admin.register(ProductColorImage)
class ProductColorImageAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    class Meta:
        model = ProductColorImage


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSizeStock)
admin.site.register(Order)
admin.site.register(OrderProducts)
admin.site.register(Contact)
admin.site.register(PopularProduct)
