# Generated by Django 3.0.5 on 2020-08-30 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0030_auto_20200830_0452'),
    ]

    operations = [

        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.CharField(default='', max_length=500),
        ),
    ]
