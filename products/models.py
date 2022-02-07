from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=20)
    
    class Meta:
        db_table = "categories"

class Color(models.Model):
    name = models.CharField(max_length=20)
    
    class Meta:
        db_table = "colors"

class Gender(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "genders"

class Country(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "countries"

class Size(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "sizes"

class Material(models.Model):
    name = models.CharField(max_length=50)

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

class ProductColor(models.Model):
    product        = models.ForeignKey(Product, on_delete=models.CASCADE)
    color          = models.ForeignKey(Color, on_delete=models.CASCADE)
    product_number = models.CharField(max_length=20)
    material       = models.ForeignKey(Material, on_delete=models.CASCADE)

    class Meta:
        db_table = "products_colors"

class ProductImage(models.Model):
    image_url     = models.URLField(max_length = 16000)
    product_color = models.ForeignKey(
        ProductColor, 
        on_delete    = models.CASCADE, 
        related_name = "products_images"
        )

    class Meta:
        db_table = "products_images"

class ColorThumbnail(models.Model):
    image_url     = models.URLField(max_length = 2000)
    product_color = models.ForeignKey(
        ProductColor, 
        on_delete    = models.CASCADE, 
        related_name = "colors_thumbnails"
        )
    
    class Meta:
        db_table = "colors_thumbnails"

class ProductOption(models.Model):
    product_color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    size          = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock         = models.IntegerField()

    class Meta:
        db_table = "products_options"