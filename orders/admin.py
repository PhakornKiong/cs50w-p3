from django.contrib import admin
from .models import Pizza, Topping, Item, Category, PizzaOrder, ItemOrder, Order, ToppingOrder
# Register your models here.
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(PizzaOrder)
admin.site.register(ItemOrder)
admin.site.register(ToppingOrder)
admin.site.register(Order)
