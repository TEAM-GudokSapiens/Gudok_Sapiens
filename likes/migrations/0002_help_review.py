<<<<<<< HEAD
<<<<<<< HEAD
# Generated by Django 3.2.6 on 2021-08-19 09:23
=======
# Generated by Django 3.2.6 on 2021-08-20 09:20
>>>>>>> service_list
=======
# Generated by Django 3.2.6 on 2021-08-20 09:54
>>>>>>> community

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('likes', '0001_initial'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='help',
            name='review',
            field=models.ForeignKey(db_column='review_id', on_delete=django.db.models.deletion.CASCADE, related_name='reviews_help', to='reviews.review'),
        ),
    ]
