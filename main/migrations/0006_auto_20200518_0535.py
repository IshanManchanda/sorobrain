# Generated by Django 3.0.5 on 2020-05-18 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200518_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='private/user_data/avatars'),
        ),
    ]
