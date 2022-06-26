from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(instance, created, *args, **kwargs):
    """Create a profile upon user registration"""

    if created:
        Profile.objects.create(user=instance)
