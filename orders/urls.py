from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("addItem/<str:ref>/<str:price>", views.addItem, name="addItem"),
    path("addPizza/<str:ref>/<str:price>", views.addPizza, name="addPizza"),
    path("addTopping/<str:ref>", views.addTopping, name="addTopping"),
    path("cart", views.cart, name="cart"),
    path("removeItem/<str:ref>", views.removeItem, name="removeItem"),
    path("removePizza/<str:ref>", views.removePizza, name="removePizza"),
    path("removeTopping/<str:ref>", views.removeTopping, name="removeTopping"),
    path("checkout", views.checkout, name="checkout"),
    path("order", views.order, name="order"),
    path("orderDetail/<str:ref>", views.orderDetail, name="orderDetail"),
    path("orderManager", views.orderManager, name="orderManager"),
    path("orderComplete/<str:ref>", views.orderComplete, name="orderComplete")
]
