# Generated by Django 5.0.2 on 2024-08-22 23:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dblfeature', '0014_alter_tmdbindex_popular_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmdbindex',
            name='popular_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]