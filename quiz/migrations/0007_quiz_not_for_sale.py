# Generated by Django 3.1 on 2021-01-03 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_auto_20210103_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='not_for_sale',
            field=models.BooleanField(default=False, verbose_name='Not For Sale'),
        ),
    ]
