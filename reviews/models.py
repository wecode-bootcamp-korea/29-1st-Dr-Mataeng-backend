from django.db import models

from users.models    import User
from products.models import ProductColor
from core.models     import TimeStampModel

class Review(TimeStampModel):
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    product_color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    title         = models.CharField(max_length=50)
    content       = models.TextField(null=True)
    image_url     = models.URLField(null=True)
    rating        = models.IntegerField()
    order_size    = models.IntegerField()

    class Meta:
        db_table = "reviews"