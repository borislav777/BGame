from django.contrib import admin

from BGame.games_rental.models import Platform, Genre, Game, Review, Slider


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(Slider)
class SlideBarAdmin(admin.ModelAdmin):
    pass
