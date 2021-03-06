# Generated by Django 4.0.3 on 2022-04-09 12:59

import common.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games_rental', '0026_slidebar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.ImageField(upload_to='games', validators=[common.validators.ValidateFileMaxSizeInMb(7)]),
        ),
    ]
