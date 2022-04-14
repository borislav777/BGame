import cloudinary.uploader
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
    cloudinary.uploader.destroy(instance.image.public_id)


@receiver(signals.pre_delete, sender=BGameUser)
def profile_image_delete(instance, **kwargs):

    cloudinary.uploader.destroy(instance.profile.picture.public_id)


@receiver(signals.pre_save, sender=Game)
def pre_save_game_image(instance, **kwargs):
    try:
        old_img = instance.__class__.objects.get(id=instance.id).image.public_id
        try:
            new_img = instance.image.public_id
        except:
            new_img = None
        if new_img != old_img and old_img:
            cloudinary.uploader.destroy(old_img)

    except:
        pass
