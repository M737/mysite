# Generated by Django 2.0.4 on 2018-07-21 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_bind',
            field=models.BooleanField(default=False),
        ),
    ]
