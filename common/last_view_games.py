from BGame.games_rental.models import Game


def get_last_viewed_games(self):
    return [Game.objects.get(pk=pk) for pk in self.request.session['last_viewed_games']][
           1::] if self.request.session.get('last_viewed_games') else []
