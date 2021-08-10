# Generated by Django 3.2.6 on 2021-08-10 02:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('likes', '0002_initial'),
        ('services', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='dib',
            name='service',
            field=models.ForeignKey(db_column='service_id', on_delete=django.db.models.deletion.CASCADE, to='services.service'),
        ),
        migrations.AddField(
            model_name='dib',
            name='users',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='users_dibs', to=settings.AUTH_USER_MODEL),
        ),
    ]
