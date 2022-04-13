from importlib import import_module
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from BGame.games_rental.models import Review, CustomerGameRent, Like
from common.tests_helpers import create_user, create_game, VALID_USER_CREDENTIALS


class GameDetailsViewTests(TestCase):
    def setUp(self):
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

    def test_review_game_form_is_valid(self):
        user = create_user()
        game = create_game()

        self.client.login(**VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('game details', kwargs={'pk': game.pk}))
        self.assertTrue(response.context['form'])

    def test_redirect_to_game_details_after_post_review(self):
        user = create_user()
        game = create_game()

        self.client.login(**VALID_USER_CREDENTIALS)

        data = {
            'title': 'hjhkhjkh',
        }

        response = self.client.post(reverse('game details', kwargs={'pk': game.pk}), data=data)
        self.assertEqual(response['location'], reverse('game details', kwargs={'pk': game.pk}))

    def test_when_has_game_reviews_expect_return_reviews(self):
        user = create_user()
        game = create_game()
        self.client.login(**VALID_USER_CREDENTIALS)

        review = Review.objects.create(
            title='Nice game',
            user=user,
            game=game,
        )
        review.save()
        response = self.client.get(reverse('game details', kwargs={'pk': game.pk}))
        reviews = [el for el in response.context['game_reviews']]

        self.assertListEqual(reviews, [review])

    def test_when_no_game_reviews_expect_return_empty_list(self):
        user = create_user()
        game = create_game()
        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('game details', kwargs={'pk': game.pk}))
        reviews = [el for el in response.context['game_reviews']]

        self.assertListEqual(reviews, [])

    def test_when_has_last_viewed_games_expect_return_games(self):
        user = create_user()
        game = create_game()
        self.client.login(**VALID_USER_CREDENTIALS)
        session = self.client.session
        games = [create_game() for _ in range(5)]

        response = self.client.get(reverse('game details', kwargs={'pk': game.pk}))
        expect_games = [g for g in games for pk in session['last_viewed_games'] if g.pk == pk][1::]

        self.assertListEqual(response.context['last_viewed_games'], expect_games)

    def test_when_no_last_viewed_games_expect_return_empty_list(self):
        user = create_user()
        game = create_game()
        self.client.login(**VALID_USER_CREDENTIALS)
        session = self.client.session
        games = [create_game() for _ in range(5)]
        session['last_viewed_games'] = []
        session.save()
        response = self.client.get(reverse('game details', kwargs={'pk': game.pk}))
        expect_games = [g for g in games for pk in session['last_viewed_games'] if g.pk == pk][1::]

        self.assertListEqual(response.context['last_viewed_games'], expect_games)

    def test_when_is_already_rented_expect_list_with_one_element(self):
        user = create_user()
        game = create_game()
        self.client.login(**VALID_USER_CREDENTIALS)

        rent = CustomerGameRent.objects.create(
            user=user,
            game=game,
        )
        rent.save()
        response = self.client.get(reverse('game details', kwargs={'pk': game.pk}))
        rented_games = [el for el in response.context['is_already_rented']]

        self.assertListEqual(rented_games, [rent])

    def test_when_is_already_rented_expect_empty_list(self):
        user = create_user()
        game = create_game()
        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('game details', kwargs={'pk': game.pk}))
        rented_games = [el for el in response.context['is_already_rented']]

        self.assertListEqual(rented_games, [])

    def test_when_is_already_liked_expect_list_with_one_element(self):
        user = create_user()
        game = create_game()
        self.client.login(**VALID_USER_CREDENTIALS)

        like = Like.objects.create(
            user=user,
            game=game,
        )
        like.save()
        response = self.client.get(reverse('game details', kwargs={'pk': game.pk}))
        likes = [el for el in response.context['is_already_liked']]

        self.assertListEqual(likes, [like])

    def test_when_is_already_liked_expect_empty_list(self):
        user = create_user()
        game = create_game()
        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('game details', kwargs={'pk': game.pk}))
        likes = [el for el in response.context['is_already_liked']]

        self.assertListEqual(likes, [])


class RentGameViewTests(TestCase):

    def test_when_is_already_rented_expect_list_with_one_element(self):
        user = create_user()
        game = create_game()
        self.client.login(**VALID_USER_CREDENTIALS)

        rent = CustomerGameRent.objects.create(
            user=user,
            game=game,
        )
        rent.save()
        response = self.client.get(reverse('rent game', kwargs={'pk': game.pk}))
        rented_games = [el for el in response.context['is_already_rented']]

        self.assertListEqual(rented_games, [rent])

    def test_when_is_already_rented_expect_empty_list(self):
        user = create_user()
        game = create_game()
        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('rent game', kwargs={'pk': game.pk}))
        rented_games = [el for el in response.context['is_already_rented']]

        self.assertListEqual(rented_games, [])


class LikeGameView(TestCase):

    def test_when_user_not_like_game(self):
        user = create_user()
        game = create_game()
        self.client.login(**VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('like game', kwargs={'pk': game.pk}))
        likes = Like.objects.get(pk=user.pk)

        self.assertTrue(likes)

        game.likes += 1
        self.assertEqual(game.likes, 1)

    def test_when_user_already_like_game(self):
        user = create_user()
        game = create_game()
        self.client.login(**VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('like game', kwargs={'pk': game.pk}))

        self.assertRedirects(response, reverse('game details', kwargs={'pk': game.pk}))
