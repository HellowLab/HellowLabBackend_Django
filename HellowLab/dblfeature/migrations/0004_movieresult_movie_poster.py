# Generated by Django 5.0.2 on 2024-08-10 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dblfeature', '0003_rename_tmdb_result_movieresult_tmdb_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='movieresult',
            name='movie_poster',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
