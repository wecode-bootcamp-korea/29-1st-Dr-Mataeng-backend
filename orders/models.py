from django.db import models

from users.models    import User
from products.models import ProductOption
from cores.models    import TimeStampModel

class Cart(TimeStampModel):
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    quantity       = models.IntegerField()

    class Meta:
        db_table = "carts"

class OrderStatus(models.Model):
    status = models.CharField(max_length=20)

    class Meta:
        db_table = "orders_stauses"

class Order(TimeStampModel):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)

    class Meta:
        db_table = "orders"

class OrderItem(TimeStampModel):
    order          = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    quantity       = models.IntegerField()
    order_status   = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)

    class Meta:
        db_table = "orders_items"