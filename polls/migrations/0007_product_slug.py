# Generated by Django 3.0.5 on 2020-08-05 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_cart_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='', max_length=40),
        ),
    ]
