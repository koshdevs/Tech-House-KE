from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import StoreSales


@receiver(post_delete, sender=StoreSales, dispatch_uid='post_deleted')
def object_post_delete_handler(sender, **kwargs):
     cache.delete('items-on-sale')


@receiver(post_save, sender=StoreSales, dispatch_uid='posts_updated')
def object_post_save_handler(sender, **kwargs):

    """
    Handles the post-save signal for the StoreSales model.

    This function is triggered whenever a StoreSales instance is saved,
    and it clears the 'items-on-sale' cache to ensure that the cache
    reflects the latest data.
    """


    cache.delete('items-on-sale')