# Generated by Django 4.0.1 on 2022-02-07 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_colorthumbnail_product_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcolor',
            name='like',
            field=models.IntegerField(default='0'),
        ),
    ]