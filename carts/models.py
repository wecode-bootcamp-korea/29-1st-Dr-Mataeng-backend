from django.db import models

from users.models    import User
from products.models import ProductOption
from core.models     import TimeStampModel

class Cart(TimeStampModel):
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    quantity       = models.IntegerField()

    class Meta:
        db_table = "carts"