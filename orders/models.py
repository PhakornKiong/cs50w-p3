from django.db import models
from django.contrib.auth.models import User
# https://www.merixstudio.com/blog/django-models-declaring-list-available-choices-right-way/
# Availability to access available choices using "variables"
Sic = "Sicilian"
Reg = "Regular"

STYLES = (
    (Sic, "Sicilian"),
    (Reg, "Regular")
)

Processing = "Processing"
Completed = "Completed"
Ordering = "Ordering"

STATUS = (
    (Ordering, "Ordering"),
    (Processing, "Processing"),
    (Completed, "Completed")
)

# Category of Item sold
class Category(models.Model):
    name=models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

# General Table for Non-Pizza Item
class Item(models.Model):
    name = models.CharField(max_length=50)
    small_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Price in USD"
    )
    # Null for item without sizes
    big_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Price in USD",
        null=True,
        blank=True
    )
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        if self.big_price == None:
            return f"{self.category} - {self.name} - Small: {self.small_price} - $"
        else:
            return f"{self.category} - {self.name} - Small: {self.small_price} - $ Big: {self.big_price} - $"

class Topping(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.name}"

class Pizza(models.Model):
    style = models.CharField(
        max_length=20,
        choices=STYLES
    )
    name = models.CharField(
        max_length=20,
    )
    small_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Price in USD"
    )
    big_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Price in USD"
    )
    max_topping=models.IntegerField(default=0)

    def __str__(self):
        if self.max_topping == 0:
            return f"{self.style} Pizza - {self.name} - Small: {self.small_price} - $ Big: {self.big_price} - $"
        else:
            return f"{self.style} Pizza - {self.name} - Small: {self.small_price} - $ Big: {self.big_price} - $ Max Topping: {self.max_topping}"

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS
    )
    total_price = models.DecimalField(
            max_digits=5,
            decimal_places=2,
            help_text="Price in USD",
            null=True,
            blank=True
    )

    def __str__(self):
        return f"{self.user} current status: {self.status}"

class PizzaOrder(models.Model):
    topping = models.IntegerField(default=0)
    pizza_ref = models.ForeignKey(Pizza,on_delete=models.CASCADE)
    order_number = models.ForeignKey(Order,on_delete=models.CASCADE)
    order_price = models.DecimalField(
            max_digits=5,
            decimal_places=2,
            help_text="Price in USD"
    )

    def __str__(self):
        return f"{self.order_number} priceL {self.order_price}"

class ItemOrder(models.Model):
    item_ref = models.ForeignKey(Item,on_delete=models.CASCADE)
    order_number = models.ForeignKey(Order,on_delete=models.CASCADE)
    order_price = models.DecimalField(
                max_digits=5,
                decimal_places=2,
                help_text="Price in USD"
    )

    def __str__(self):
        return f"{self.order_number} priceL {self.order_price}"

class ToppingOrder(models.Model):
    topping_ref = models.ForeignKey(Topping,on_delete=models.CASCADE)
    order_number = models.ForeignKey(Order,on_delete=models.CASCADE)
    pizza_order_ref = models.ForeignKey(PizzaOrder,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.topping_ref} to {self.pizza_order_ref} to order {self.order_number}"
