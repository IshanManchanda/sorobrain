# Generated by Django 3.0.5 on 2020-05-27 07:52

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('workshops', '0004_workshopaccess'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]