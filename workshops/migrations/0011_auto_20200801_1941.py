# Generated by Django 3.0.7 on 2020-08-01 14:11

import django.core.validators
from django.db import migrations, models
import sorobrain.media_storages


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0010_workshop_related_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='related_file',
            field=models.FileField(blank=True, null=True, storage=sorobrain.media_storages.PrivateMediaStorage(), upload_to='workshops/files/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]
