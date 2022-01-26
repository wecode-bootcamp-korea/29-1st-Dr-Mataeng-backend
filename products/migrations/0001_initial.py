# Generated by Django 4.0.1 on 2022-01-26 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'colors',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'genders',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'materials',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=3, max_digits=30)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.country')),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.gender')),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='Product_Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_number', models.CharField(max_length=20)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.color')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.material')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'db_table': 'products_colors',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'sizes',
            },
        ),
        migrations.CreateModel(
            name='Product_Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.IntegerField()),
                ('product_color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product_color')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.size')),
            ],
            options={
                'db_table': 'products_options',
            },
        ),
        migrations.CreateModel(
            name='Product_Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(max_length=16000)),
                ('product_color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product_color')),
            ],
            options={
                'db_table': 'products_images',
            },
        ),
        migrations.CreateModel(
            name='Color_Thumbnail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(max_length=2000)),
                ('product_color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product_color')),
            ],
            options={
                'db_table': 'colors_thumbnails',
            },
        ),
    ]