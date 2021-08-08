# Generated by Django 3.2.6 on 2021-08-08 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
        ('reviews', '0002_alter_review_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services_review', to='services.service', verbose_name='서비스'),
        ),
    ]
