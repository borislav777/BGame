from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy
from django.views import generic as views

from BGame.games_rental.forms import AddGameForm, EditGameForm, EditSliderForm, AddGenreForm, AddPlatformForm, \
    AddSliderForm
from BGame.games_rental.models import Game, Slider, Genre, Platform
from common.mixins import StaffRequiredMixin


class AddGameView(StaffRequiredMixin, views.CreateView):
    form_class = AddGameForm
    template_name = 'games_rental/add_game.html'
    success_url = reverse_lazy('index')


class EditGameView(StaffRequiredMixin, views.UpdateView):
    model = Game
    form_class = EditGameForm
    template_name = 'games_rental/edit_game.html'

    def get_success_url(self):
        return reverse_lazy('game details', kwargs={'pk': self.object.pk})


class DeleteGameView(StaffRequiredMixin, views.DeleteView):
    model = Game
    template_name = 'games_rental/delete_game.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        session = self.request.session['last_viewed_games']
        if pk in self.request.session['last_viewed_games']:
            self.request.session['last_viewed_games'].remove(pk)
            self.request.session['last_viewed_games'] = session

        result = super().dispatch(request, *args, **kwargs)

        return result


class AddGenreView(StaffRequiredMixin, views.CreateView):
    model = Genre
    form_class = AddGenreForm
    template_name = 'games_rental/add_genre.html'
    success_url = reverse_lazy('index')


class AddPlatformView(StaffRequiredMixin, views.CreateView):
    model = Platform
    form_class = AddPlatformForm
    template_name = 'games_rental/add_platform.html'
    success_url = reverse_lazy('index')


class AddSliderView(StaffRequiredMixin, views.CreateView):

    model = Slider
    form_class = AddSliderForm
    template_name = 'games_rental/add_slider.html'
    success_url = reverse_lazy('index')


class EditSliderView(StaffRequiredMixin, views.UpdateView):

    model = Slider
    form_class = EditSliderForm
    template_name = 'games_rental/edit_slider.html'
    success_url = reverse_lazy('index')
