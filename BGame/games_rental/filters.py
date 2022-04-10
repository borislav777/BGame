import django_filters

from BGame.games_rental.models import Game


class GamesFilter(django_filters.FilterSet):
    CHOICES = (
        ('name', 'A-Z'),
        ('-name', 'Z-A'),
        ('-release_date', 'New'),
        ('platform', 'Platform'),
    )

    ordering = django_filters.ChoiceFilter(label='Order By:', choices=CHOICES, method='filter_by_order')

    class Meta:
        model = Game
        fields = ()

    def filter_by_order(self, queryset, name, value):
        return queryset.order_by(value)
