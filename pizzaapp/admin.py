from django.contrib import admin
from .models import pizza,Cart,Order

# Register your models here.

class PizzaAdmin(admin.ModelAdmin):
    list_display=['sno','pizza_name','pizza_desc','pizza_price','image']

admin.site.register(pizza,PizzaAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display=['sno','qty','userid']

admin.site.register(Cart,CartAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display=['order_id','userid','sno','qty']

admin.site.register(Order,OrderAdmin)