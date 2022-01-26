from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=50)
    username     = models.CharField(max_length=100, unique=True)
    password     = models.CharField(max_length=200)
    birthday     = models.DateField()
    email        = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=30)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
  
    class Meta:
        db_table = "users"
