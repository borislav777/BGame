# Generated by Django 4.0.3 on 2022-04-09 12:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0009_remove_profile_email_bgameuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='budget',
            field=models.IntegerField(blank=True, default=100, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
