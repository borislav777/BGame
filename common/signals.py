from django.db.models import signals
from django.dispatch import receiver
import os

from BGame.auth_app.models import BGameUser
from BGame.games_rental.models import CustomerGameRent, Game


@receiver(signals.pre_save, sender=CustomerGameRent)
def rent_post_created(instance, **kwargs):
    profile = instance.user.profile
    profile.budget -= instance.amount
    profile.save()


@receiver(signals.post_delete, sender=Game)
def game_delete(instance, **kwargs):
    os.remove(instance.image.path)


@receiver(signals.pre_delete, sender=BGameUser)
def profile_image_delete(instance, **kwargs):
    os.remove(instance.profile.picture.path)


@receiver(signals.pre_save, sender=Game)
def pre_save_game_image(instance, **kwargs):
    try:
        old_img = instance.__class__.objects.get(id=instance.id).image.path
        try:
            new_img = instance.image.path
        except:
            new_img = None
        if new_img != old_img:
            import os
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass
