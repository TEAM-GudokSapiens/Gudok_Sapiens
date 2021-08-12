# Generated by Django 3.2.6 on 2021-08-10 07:29

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('community', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(validators=[django.core.validators.MinLengthValidator(15)], verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='삭제여부')),
                ('reply', models.IntegerField(default=0, verbose_name='답글위치')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='community.board', verbose_name='게시글')),
            ],
            options={
                'verbose_name': '자유게시판 댓글',
                'verbose_name_plural': '자유게시판 댓글',
                'db_table': '자유게시판 댓글',
            },
        ),
    ]
