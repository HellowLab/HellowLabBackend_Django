# Generated by Django 5.0.2 on 2024-08-15 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dblfeature', '0006_alter_movieresult_mycomments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movieresult',
            name='liked',
            field=models.BooleanField(null=True),
        ),
    ]
