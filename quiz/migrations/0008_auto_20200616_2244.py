# Generated by Django 3.0.5 on 2020-06-16 17:14

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_auto_20200616_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizsubmission',
            name='submission',
            field=django.contrib.postgres.fields.jsonb.JSONField(default='{}', null=True),
        ),
    ]
