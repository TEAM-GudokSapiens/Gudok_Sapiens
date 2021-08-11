# Generated by Django 3.2.6 on 2021-08-10 07:29

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0001_initial'),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
