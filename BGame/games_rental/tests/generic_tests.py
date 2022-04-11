from importlib import import_module

from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.test import RequestFactory
from django.urls import reverse

from common.tests_helpers import create_game, create_user, VALID_USER_CREDENTIALS

factory = RequestFactory()


class HomeViewTests(TestCase):

    def test_expect_correct_template(self):
        self.client.get(reverse('index'))
        self.assertTemplateUsed('games_rental/index.html')

    def test_when_games_list_return_four_games(self):
        games = [create_game() for _ in range(7)][:4]

        self.assertEqual(4, len(games))


class CatalogueViewTests(TestCase):

    def setUp(self):
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

    def test_expect_correct_template(self):
        self.client.get(reverse('catalogue'))
        self.assertTemplateUsed('games_rental/catalogue.html')

    def test_when_has_last_viewed_games_expect_return_games(self):
        user = create_user()
        self.client.login(**VALID_USER_CREDENTIALS)
        session = self.client.session
        games = [create_game() for _ in range(5)]
        session['last_viewed_games'] = [g.pk for g in games][:2]
        session.save()
        response = self.client.get(reverse('catalogue'))
        expect_games = [g for g in games for pk in session['last_viewed_games'] if g.pk == pk][1::]

        self.assertListEqual(response.context['last_viewed_games'], expect_games)

    def test_when_no_last_viewed_games_expect_return_empty_list(self):
        user = create_user()
        self.client.login(**VALID_USER_CREDENTIALS)
        session = self.client.session
        games = [create_game() for _ in range(5)]
        session['last_viewed_games'] = []
        session.save()
        response = self.client.get(reverse('catalogue'))
        expect_games = [g for g in games for pk in session['last_viewed_games'] if g.pk == pk][1::]

        self.assertListEqual(response.context['last_viewed_games'], expect_games)


class ContactTests(TestCase):

    def test_send_email(self):
        user = create_user()
        self.client.login(**VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('contact'))

        mail.send_mail('HI', 'Message',
                       'peter@abv.bg', ['info.bggame@gmail.com'],
                       fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'HI')
        self.assertEqual(mail.outbox[0].from_email, 'peter@abv.bg')
        self.assertEqual(mail.outbox[0].to, ['info.bggame@gmail.com'])
        self.assertEqual(mail.outbox[0].body, 'Message')
