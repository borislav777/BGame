# Generated by Django 4.0.3 on 2022-04-05 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games_rental', '0003_alter_game_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_released',
            field=models.BooleanField(default=True),
        ),
    ]