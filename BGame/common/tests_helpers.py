import random
import datetime

from BGame.auth_app.models import BGameUser, Profile
from BGame.games_rental.models import Genre, Platform, Game

VALID_USER_CREDENTIALS = {
    'username': 'Test',
    'password': 'Tk123456',
}


def create_game():
    genre = Genre.objects.create(name='Action')
    platform = Platform.objects.create(name='PS5')
    return Game.objects.create(
        name=f'Test{random.random()}',
        publisher='Sony',
        release_date=datetime.date(2022, 1, 20),
        description='Nice game',
        image='image.jpg',
        genre=genre,
        platform=platform,
    )


def create_user():
    user = BGameUser.objects.create(
        username='Test',
        email='test@abv.bg',
        is_active=True,
    )
    user.set_password('Tk123456')
    profile = Profile.objects.create(

        first_name='Test',
        last_name='Testov',
        picture='image.jpg',
        user=user,
    )
    user.profile = profile
    user.save()

    return user
