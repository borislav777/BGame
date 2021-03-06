# Generated by Django 4.0.3 on 2022-04-14 08:47

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games_rental', '0033_remove_game_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='image',
            field=cloudinary.models.CloudinaryField(default=2006, max_length=255, verbose_name='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='slider',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
