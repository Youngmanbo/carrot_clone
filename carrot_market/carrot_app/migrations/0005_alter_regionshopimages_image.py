# Generated by Django 4.2.5 on 2023-10-01 09:27

import carrot_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrot_app', '0004_alter_regionshop_thumnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regionshopimages',
            name='image',
            field=models.ImageField(upload_to=carrot_app.models.image_upload),
        ),
    ]
