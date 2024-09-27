# Generated by Django 5.0.2 on 2024-08-14 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_friendrequest_friendship'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendship',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Accepted'), ('R', 'Rejected')], default='P', max_length=1),
        ),
    ]
