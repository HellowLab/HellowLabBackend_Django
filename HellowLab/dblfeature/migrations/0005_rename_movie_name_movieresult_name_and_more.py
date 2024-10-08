# Generated by Django 5.0.2 on 2024-08-11 14:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dblfeature', '0004_movieresult_movie_poster'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='movieresult',
            old_name='movie_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='movieresult',
            old_name='movie_poster',
            new_name='poster',
        ),
        migrations.AlterField(
            model_name='movieresult',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
