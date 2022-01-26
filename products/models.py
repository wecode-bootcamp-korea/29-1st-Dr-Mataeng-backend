from django.db import models

class Category(models.Model):
    category = models.CharField(max_length=20)
    
    class Meta:
        db_table = "categories"

class Color(models.Model):
    color = models.CharField(max_length=20)
    
    class Meta:
        db_table = "colors"

class Gender(models.Model):
    gender = models.CharField(max_length=20)

    class Meta:
        db_table = "genders"

class Country(models.Model):
    country = models.CharField(max_length=100)

    class Meta:
        db_table = "countries"

class Size(models.Model):
    size = models.CharField(max_length=20)

    class Meta:
        db_table = "sizes"

class Material(models.Model):
    material = models.CharField(max_length=50)

    class Meta:
        db_table = "materials"

class Product(models.Model):
    name     = models.CharField(max_length=50)
    price    = models.DecimalField(max_digits=30, decimal_places=3)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    country  = models.ForeignKey(Country, on_delete=models.CASCADE)
    gender   = models.ForeignKey(Gender, on_delete=models.CASCADE)

    class Meta:
        db_table = "products"

class Product_Color(models.Model):
    product        = models.ForeignKey(Product, on_delete=models.CASCADE)
    color          = models.ForeignKey(Color, on_delete=models.CASCADE)
    product_number = models.CharField(max_length=20)
    material       = models.ForeignKey(Material, on_delete=models.CASCADE)

    class Meta:
        db_table = "products_colors"

class Product_Image(models.Model):
    image_url     = models.URLField(max_length = 16000)
    product_color = models.ForeignKey(Product_Color, on_delete=models.CASCADE)

    class Meta:
        db_table = "products_images"

class Color_Thumbnail(models.Model):
    image_url     = models.URLField(max_length = 2000)
    product_color = models.ForeignKey(Product_Color, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "colors_thumbnails"

class Product_Option(models.Model):
    product_color = models.ForeignKey(Product_Color, on_delete=models.CASCADE)
    size          = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock         = models.IntegerField()

    class Meta:
        db_table = "products_options"