import datetime

from django.urls import reverse_lazy
from django.views import generic as views

from BGame.games_rental.filters import GamesFilter
from BGame.games_rental.forms import ContactForm
from BGame.games_rental.models import Game, Slider
from common.amount import PRICE_PER_DAY
from common.last_view_games import get_last_viewed_games
from django.core.mail import send_mail

from common.mixins import LoginRequired


class HomeView(views.ListView):
    model = Game
    template_name = 'games_rental/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        slider = Slider.objects.all()
        price_per_day = PRICE_PER_DAY
        popular = self.object_list.order_by('-likes')[:4]
        coming = self.model.objects.filter(release_date__gt=datetime.date.today())[:4]
        recently_added = self.object_list.order_by('-add_date')[:4]
        context.update({
            'popular': popular,
            'coming': coming,
            'recently_added': recently_added,
            'slider': slider,
            'price_per_day': price_per_day,
        })

        return context


class CatalogueView(LoginRequired, views.ListView):

    model = Game
    template_name = 'games_rental/catalogue.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        last_viewed_games = get_last_viewed_games(self)
        filters = GamesFilter(self.request.GET, queryset=self.get_queryset())
        price_per_day = PRICE_PER_DAY
        order_by = self.request.GET.get('ordering')
        context = super().get_context_data(**kwargs)
        context.update({

            'last_viewed_games': last_viewed_games,
            'filters': filters,
            'order_by': order_by,
            'price_per_day': price_per_day,

        })

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return GamesFilter(self.request.GET, queryset=queryset).qs


class Contact(LoginRequired, views.FormView):
    form_class = ContactForm
    template_name = 'games_rental/contact.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        from_mail = form.cleaned_data.get('from_mail')
        subject = form.cleaned_data.get('subject')
        message = form.cleaned_data.get('message')
        send_mail(subject, message, from_mail, ['info.bggame@gmail.com', from_mail])

        return super().form_valid(form)
