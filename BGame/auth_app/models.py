from django.contrib.auth import models as auth_models
from django.core.validators import RegexValidator, MinLengthValidator, MinValueValidator
from django.db import models

from BGame.auth_app.managers import BGameUserManager
from common.validators import validate_only_letters, ValidateFileMaxSizeInMb


class BGameUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_MAX_LENGTH = 30

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=(
            RegexValidator(r'^[0-9a-zA-Z\_]*$', "Ensure this value contains only letters, numbers, and underscore."),
            MinLengthValidator(2),
        )
    )

    email = models.EmailField(
        unique=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    USERNAME_FIELD = 'username'
    objects = BGameUserManager()


class Profile(models.Model):
    FIRST_NAME_MIN_LENGTH = 3
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 3
    LAST_NAME_MAX_LENGTH = 30

    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do not show'

    GENDERS = [(g, g) for g in (MALE, FEMALE, DO_NOT_SHOW)]

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    gender = models.CharField(
        choices=GENDERS,
        max_length=20,
        blank=True,
    )

    picture = models.ImageField(
        upload_to='profile',
        validators=(
            ValidateFileMaxSizeInMb(5),
        )
    )

    description = models.TextField(
        null=True,
        blank=True,

    )

    budget = models.IntegerField(
        default=100,
        validators=(
            MinValueValidator(0),
        ),
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        BGameUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
