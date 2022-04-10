from django.urls import path

from BGame.games_rental.views.admin_views import AddGameView, EditGameView, DeleteGameView, AddGenreView, \
    AddPlatformView, AddSliderView, EditSliderView
from BGame.games_rental.views.game_views import GameDetailsView, RentGameView, \
    like_game_view, ReturnGameView
from BGame.games_rental.views.generic import HomeView, CatalogueView, Contact

urlpatterns = (
    path('', HomeView.as_view(), name='index'),
    path('catalogue/', CatalogueView.as_view(), name='catalogue'),

    path('contact/', Contact.as_view(), name='contact'),

    path('game/add/', AddGameView.as_view(), name='add game'),
    path('game/edit/<int:pk>', EditGameView.as_view(), name='edit game'),
    path('game/delete/<int:pk>', DeleteGameView.as_view(), name='delete game'),

    path('genre/add/', AddGenreView.as_view(), name='add genre'),
    path('platform/add/', AddPlatformView.as_view(), name='add platform'),
    path('slidebar/add/', AddSliderView.as_view(), name='add slidebar'),
    path('slidebar/edit/<int:pk>', EditSliderView.as_view(), name='edit slidebar'),

    path('game/details/<int:pk>', GameDetailsView.as_view(), name='game details'),
    path('game/rent/<int:pk>', RentGameView.as_view(), name='rent game'),
    path('game/return/<int:pk>', ReturnGameView.as_view(), name='return game'),


    path('game/like/<int:pk>', like_game_view, name='like game'),

)
