from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from BGame.games_rental.forms import ReviewGameForm, RentGameForm
from BGame.games_rental.models import Game, Like, Review, CustomerGameRent
from common.last_view_games import get_last_viewed_games
from common.mixins import LoginRequired


class GameDetailsView(LoginRequired, views.DetailView):
    model = Game
    template_name = 'games_rental/game_details.html'
    form = ReviewGameForm

    def post(self, request, *args, **kwargs):
        form = ReviewGameForm(request.POST)
        if form.is_valid():
            game = self.get_object()
            form.instance.user = request.user
            form.instance.game = game
            form.save()
            return redirect(reverse('game details', kwargs={'pk': game.pk}))

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj

    def get_success_url(self):
        return reverse_lazy('game details', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        game_reviews = Review.objects.all().filter(game_id=self.object.id)
        last_viewed_games = get_last_viewed_games(self)
        is_already_rented = CustomerGameRent.objects.filter(game_id=self.kwargs.get('pk'))
        is_already_liked = Like.objects.filter(user_id=self.request.user, game_id=self.kwargs.get('pk'))

        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.form,
            'game_reviews': game_reviews,
            'last_viewed_games': last_viewed_games,
            'is_already_rented': is_already_rented,
            'is_already_liked': is_already_liked,
        })

        return context

    def dispatch(self, request, *args, **kwargs):
        last_viewed_game = request.session.get('last_viewed_games', [])
        if self.kwargs.get('pk') not in last_viewed_game:
            last_viewed_game.insert(0, self.kwargs.get('pk'))
        request.session['last_viewed_games'] = last_viewed_game[:5]
        result = super().dispatch(request, *args, **kwargs)
        return result


class RentGameView(LoginRequired, views.CreateView):
    model = CustomerGameRent
    form_class = RentGameForm
    template_name = 'games_rental/rent_game.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        game = Game.objects.get(pk=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        is_already_rented = CustomerGameRent.objects.filter(game_id=self.kwargs.get('pk'))
        context.update({
            'game': game,
            'is_already_rented': is_already_rented,
        })

        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        initial['game'] = Game.objects.get(pk=self.kwargs.get('pk'))
        return initial


@login_required
def like_game_view(request, pk):
    new_like, created = Like.objects.get_or_create(user=request.user, game_id=pk)
    if created:
        game = Game.objects.get(pk=pk)
        game.likes += 1
        game.save()

    return redirect('game details', pk)


class ReturnGameView(LoginRequired, views.DeleteView):
    model = CustomerGameRent
    success_url = reverse_lazy('index')
