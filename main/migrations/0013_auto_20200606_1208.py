# Generated by Django 3.0.5 on 2020-06-06 06:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20200606_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookaccess',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]