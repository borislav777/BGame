# Generated by Django 4.0.3 on 2022-04-10 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games_rental', '0028_alter_game_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='rent_price_per_day',
        ),
    ]
