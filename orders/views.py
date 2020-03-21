from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse

from orders.models import Pizza, Topping, Item, Category, PizzaOrder, ItemOrder, Order, ToppingOrder


def index(request):
    """ Homepage where users can view the menu and add items to a virtual cart """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    #Check whether there are "Odering" order in order table
    order_number = get_order_num(request.user)
    print(order_number)
    context = {
        "pizzas": Pizza.objects.all(),
        "toppings": Topping.objects.all(),
        "items": Item.objects.all(),
        "categories": Category.objects.all(),
        "order_number": order_number
    }

    return render(request, "orders/index.html", context)

@login_required(login_url='/login/')
def addItem(request,ref,price):
    """ Manage the logic for add Item Order"""
    order_number = get_order_num(request.user)
    addItem=ItemOrder(
    item_ref=Item.objects.get(pk=ref),
    order_number=Order.objects.get(user_id=request.user, status="Ordering"),
    order_price=price
    )
    addItem.save()
    messages.info(request, "Item Added")
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url='/login/')
def removeItem(request,ref):
    """ Manage the logic for remove Item Order"""
    removeItem=ItemOrder.objects.filter(pk=ref)
    removeItem.delete()
    messages.info(request, "Item Removed")
    return HttpResponseRedirect(reverse("cart"))

@login_required(login_url='/login/')
def addPizza(request,ref,price):
    """ Manage the logic for add Item Order"""
    order_number = get_order_num(request.user)
    # Get max topping from pizza model
    max_topping = Pizza.objects.get(pk=ref).max_topping
    addPizza=PizzaOrder(
    pizza_ref=Pizza.objects.get(pk=ref),
    order_number=Order.objects.get(user_id=request.user, status="Ordering"),
    order_price=price,
    topping=max_topping
    )
    addPizza.save()
    messages.info(request, "Pizza Added")
    return HttpResponseRedirect(reverse("index"))

def removePizza(request,ref):
    """ Manage the logic for remove Pizza Order"""
    removePizza=PizzaOrder.objects.filter(pk=ref)
    removePizza.delete()
    messages.info(request, "Pizza Removed")
    return HttpResponseRedirect(reverse("cart"))

@login_required(login_url='/login/')
def addTopping(request,ref):
    """ Manage the logic for adding Topping"""
    order_number = get_order_num(request.user)

    try:
        pizza = PizzaOrder.objects.filter(order_number = order_number).last()
        topping_allowance = pizza.topping
    except AttributeError:
        messages.info(request, "No Pizza in Cart, Please Add One")
        return HttpResponseRedirect(reverse("index"))
    if topping_allowance != 0:
        addTopping=ToppingOrder(
        topping_ref=Topping.objects.get(pk=ref),
        pizza_order_ref=pizza,
        order_number=Order.objects.get(user_id=request.user, status="Ordering")
        )
        addTopping.save()
        topping_allowance -= 1
        update_topping = PizzaOrder.objects.filter(id=pizza.id).update(topping=topping_allowance)
        messages.info(request, "Topping Added")
        return HttpResponseRedirect(reverse("index"))
    else:
        messages.info(request, "No Topping Allowance")
    return HttpResponseRedirect(reverse("index"))

def removeTopping(request,ref):
    """ Manage the logic for remove Pizza Order"""
    order_number = get_order_num(request.user)
    removeTopping=ToppingOrder.objects.filter(pk=ref)
    removeTopping.delete()
    pizza = PizzaOrder.objects.filter(order_number = order_number).last()
    topping_allowance = pizza.topping
    topping_allowance += 1
    update_topping = PizzaOrder.objects.filter(id=pizza.id).update(topping=topping_allowance)
    messages.info(request, "Topping Removed")
    return HttpResponseRedirect(reverse("cart"))

@login_required(login_url='/login/')
def cart(request):
    order_number = get_order_num(request.user)
    context = {
        "ItemOrder": ItemOrder.objects.filter(order_number=order_number),
        "PizzaOrder": PizzaOrder.objects.filter(order_number=order_number),
        "ToppingOrder": ToppingOrder.objects.filter(order_number=order_number),
        "order_number": order_number,
        "total_price": get_total_price(request.user)
    }
    return render(request, "orders/cart.html", context)

@login_required(login_url='/login/')
def checkout(request):
    total_price = get_total_price(request.user)
    order_number = get_order_num(request.user)
    update_status = Order.objects.filter(pk=order_number).update(status="Processing", total_price=total_price)
    get_order_num(request.user)
    messages.info(request, "Checkout Successfully")
    return HttpResponseRedirect(reverse("order"))

@login_required(login_url='/login/')
def order(request):
    context = {
        "orders": Order.objects.filter(user=request.user.id),
    }
    return render(request, "orders/order.html", context)

@login_required(login_url='/login/')
def orderDetail(request,ref):
    id=Order.objects.get(pk=ref).id
    context = {
        "orders": Order.objects.get(pk=ref),
        "ItemOrder": ItemOrder.objects.filter(order_number=id),
        "PizzaOrder": PizzaOrder.objects.filter(order_number=id),
        "ToppingOrder": ToppingOrder.objects.filter(order_number=id),
        "order_number": id,
    }
    return render(request, "orders/orderDetail.html", context)

@login_required(login_url='/login/')
def orderManager(request):
    context = {
        "orders": Order.objects.all(),
    }
    return render(request, "orders/orderManager.html", context)

@login_required(login_url='/login/')
def orderComplete(request, ref):
    update_status = Order.objects.filter(pk=ref).update(status="Complete")
    messages.info(request, "Order Completed Successfully")
    return HttpResponseRedirect(reverse("orderManager"))

def get_order_num(user):
    #Check whether there are "Odering" order in order table
    try:
        check_order = Order.objects.get(user_id=user, status="Ordering").id
    except Order.DoesNotExist:
        add_order=Order(user=user, status="Ordering")
        add_order.save()

    return Order.objects.get(user_id=user, status="Ordering").id

def get_total_price(user):
    order_number = get_order_num(user)
    total_price = 0
    pizzas = PizzaOrder.objects.filter(order_number=order_number)
    for pizza in pizzas:
        total_price += pizza.order_price
    items = ItemOrder.objects.filter(order_number=order_number)
    for item in items:
        total_price += item.order_price
    return total_price
