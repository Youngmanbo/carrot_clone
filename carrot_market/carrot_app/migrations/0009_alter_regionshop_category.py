# Generated by Django 4.2.5 on 2023-10-04 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrot_app', '0008_alter_regionshop_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regionshop',
            name='category',
            field=models.CharField(choices=[('all', '전체'), ('restaurant', '식당'), ('cafe', '카페'), ('move', '이사/용달'), ('beauty', '뷰티/미용'), ('health', '헬스/필라테스/요가')], max_length=50),
        ),
    ]
