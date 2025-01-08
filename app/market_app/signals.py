from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, User
from .tasks import generate_thumbnails

@receiver(post_save, sender=Product)
def process_product_image(sender, instance, **kwargs):
    if instance.image:
        generate_thumbnails.delay(instance.image.path)

@receiver(post_save, sender=User)
def process_user_image(sender, instance, **kwargs):
    if instance.image:
        generate_thumbnails.delay(instance.image.path)