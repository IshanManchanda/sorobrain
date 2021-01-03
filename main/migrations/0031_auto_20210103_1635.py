# Generated by Django 3.1 on 2021-01-03 11:05

from django.db import migrations, models
import sorobrain.media_storages


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='ledger',
            name='balance',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='school_id',
            field=models.ImageField(blank=True, null=True, storage=sorobrain.media_storages.PrivateMediaStorage(), upload_to='user_data/school_ids/', verbose_name='ID'),
        ),
    ]
