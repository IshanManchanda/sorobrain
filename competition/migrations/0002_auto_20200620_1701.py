# Generated by Django 3.0.7 on 2020-06-20 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competitionquiz',
            options={'ordering': ('created_on',), 'verbose_name': 'Competition Quiz', 'verbose_name_plural': 'Competition Quizzes'},
        ),
    ]