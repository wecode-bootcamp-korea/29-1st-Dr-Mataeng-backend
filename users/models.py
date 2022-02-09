from django.db import models

from core.models    import TimeStampModel

class User(TimeStampModel):
    name         = models.CharField(max_length=50)
    username     = models.CharField(max_length=100, unique=True)
    password     = models.CharField(max_length=200)
    birthday     = models.DateField()
    email        = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=30)
    gender       = models.CharField(max_length=10)
    recommender  = models.CharField(max_length=100, blank=True)
    point        = models.DecimalField(max_digits=30, decimal_places=0, default = '0')

    class Meta:
        db_table = "users"