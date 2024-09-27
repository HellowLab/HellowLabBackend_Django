# Generated by Django 5.0.2 on 2024-08-17 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dblfeature', '0008_alter_movieresult_mycomments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movieresult',
            name='liked',
            field=models.PositiveIntegerField(choices=[(0, 'None'), (1, 'Liked'), (2, 'Disliked')], default=0),
        ),
    ]