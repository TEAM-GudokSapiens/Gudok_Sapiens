<<<<<<< HEAD:likes/migrations/0002_initial.py
# Generated by Django 3.2.6 on 2021-08-16 11:38
=======
# Generated by Django 3.2.6 on 2021-08-15 15:27
>>>>>>> service_list:likes/migrations/0003_initial.py

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD:likes/migrations/0002_initial.py
        ('likes', '0001_initial'),
        ('reviews', '0001_initial'),
=======
>>>>>>> service_list:likes/migrations/0003_initial.py
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('likes', '0002_help_review'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='help',
            name='review',
            field=models.ForeignKey(db_column='review_id', on_delete=django.db.models.deletion.CASCADE, related_name='reviews_help', to='reviews.review'),
        ),
        migrations.AddField(
            model_name='help',
            name='users',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='users_helps', to=settings.AUTH_USER_MODEL),
        ),
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
