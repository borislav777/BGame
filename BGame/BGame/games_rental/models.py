import django.utils.timezone

from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from common.validators import ValidateFileMaxSizeInMb

UserModel = get_user_model()


class Platform(models.Model):
    PLATFORM_NAME_MIN_LENGTH = 2
    PLATFORM_NAME_MAX_LENGTH = 10

    name = models.CharField(
        max_length=PLATFORM_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(PLATFORM_NAME_MIN_LENGTH),
        )

    )

    def __str__(self):
        return f"{self.name}"


class Genre(models.Model):
    GENRE_NAME_MIN_LENGTH = 3
    GENRE_NAME_MAX_LENGTH = 25

    name = models.CharField(
        max_length=GENRE_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(GENRE_NAME_MIN_LENGTH),
        )
    )

    def __str__(self):
        return f"{self.name}"


class Game(models.Model):
    GAME_NAME_MIN_LENGTH = 2
    GAME_NAME_MAX_LENGTH = 50

    PUBLISHER_MAX_LENGTH = 20

    name = models.CharField(
        max_length=GAME_NAME_MAX_LENGTH,
        unique=True,
        validators=(
            MinLengthValidator(GAME_NAME_MIN_LENGTH),
        )
    )

    publisher = models.CharField(
        max_length=PUBLISHER_MAX_LENGTH,
        blank=True,
        null=True,
    )

    release_date = models.DateField(

    )

    description = models.TextField()

    image = models.ImageField(
        upload_to='games',
        validators=(
            ValidateFileMaxSizeInMb(5),
        )
    )

    likes = models.IntegerField(
        default=0,
    )

    views = models.IntegerField(
        default=0,
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )

    add_date = models.DateTimeField(
        auto_now_add=True,
    )
    platform = models.ForeignKey(
        Platform,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name}"


class Review(models.Model):
    title = models.TextField()

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.game}"


class Like(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class CustomerGameRent(models.Model):
    date = models.DateField(

        default=django.utils.timezone.now,

    )
    return_date = models.DateField(
        default=django.utils.timezone.now,
    )
    amount = models.FloatField(
        default=0,
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class Slider(models.Model):
    image = models.ImageField(
        upload_to='slider',
        validators=(
            ValidateFileMaxSizeInMb(7),
        )
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.game}"
