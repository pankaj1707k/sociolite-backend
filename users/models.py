from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    A custom User model with `first_name` and `last_name` replaced with `name`.
    The `email` field is set as unique and required.
    """

    first_name = None
    last_name = None
    name = models.CharField(_("name"), max_length=300, blank=True)
    email = models.EmailField(_("email"), unique=True)
