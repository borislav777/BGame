# Generated by Django 4.0.3 on 2022-04-10 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games_rental', '0029_remove_game_rent_price_per_day'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SlideBar',
            new_name='Slider',
        ),
    ]
