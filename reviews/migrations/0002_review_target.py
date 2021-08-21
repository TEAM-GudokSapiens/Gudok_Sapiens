

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0001_initial'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='review', to='services.service', verbose_name='서비스'),
        ),
    ]
