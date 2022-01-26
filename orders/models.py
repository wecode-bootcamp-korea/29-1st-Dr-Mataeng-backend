from django.db import models

from users.models    import User
from products.models import Product_Option

class Cart(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    product_option = models.ForeignKey(Product_Option, on_delete=models.CASCADE)
    quantity       = models.IntegerField()
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "carts"

class Order_Status(models.Model):
    status = models.CharField(max_length=20)

    class Meta:
        db_table = "orders_stauses"

class Order_Item(models.Model):
    product_option = models.ForeignKey(Product_Option, on_delete=models.CASCADE)
    quantity       = models.IntegerField()
    order_status   = models.ForeignKey(Order_Status, on_delete=models.CASCADE)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders_items"

class Order(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    order_item   = models.ForeignKey(Order_Item, on_delete=models.CASCADE)
    order_status = models.ForeignKey(Order_Status, on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders"