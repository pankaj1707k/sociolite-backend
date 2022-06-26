from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.utils import get_profile_image_path


class User(AbstractUser):
    """
    A custom User model with `first_name` and `last_name` replaced with `name`.
    The `email` field is set as unique and required.
    """

    first_name = None
    last_name = None
    name = models.CharField(_("name"), max_length=300, blank=True)
    email = models.EmailField(_("email"), unique=True)


class Profile(models.Model):
    """
    Model representing the profile data associated to a User instance.
    One-to-one relation with User model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(_("location"), max_length=100, blank=True)
    work = models.CharField(_("work"), max_length=200, blank=True)
    about = models.TextField(_("about"), blank=True)
    date_of_birth = models.DateField(_("date of birth"), blank=True)
    picture = models.ImageField(
        _("picture"), upload_to=get_profile_image_path, default="profile/default.png"
    )

    def __str__(self) -> str:
        return f"{self.user.username}"
