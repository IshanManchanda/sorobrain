# Generated by Django 3.0.7 on 2020-06-27 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0003_auto_20200626_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='thumbnail',
            field=models.ImageField(blank=True, default='compete/thumbnails/default.jpg', null=True, upload_to='compete/thumbnails/'),
        ),
    ]
