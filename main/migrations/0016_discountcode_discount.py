# Generated by Django 3.0.5 on 2020-06-19 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20200619_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='discountcode',
            name='discount',
            field=models.IntegerField(default=20, verbose_name='Enter Discount Percentage, 100 for free:'),
            preserve_default=False,
        ),
    ]
