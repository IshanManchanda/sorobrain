# Generated by Django 3.1 on 2021-01-03 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0009_competition_rank_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='not_for_sale',
            field=models.BooleanField(default=False, verbose_name='Not For Sale'),
        ),
    ]
