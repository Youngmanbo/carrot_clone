# Generated by Django 4.2.5 on 2023-10-05 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrot_app', '0013_alter_regionshop_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regionshopproductprice',
            name='option',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
