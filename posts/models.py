from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from posts.utils import get_post_image_path

User = get_user_model()


class Post(models.Model):
    """
    Model representing a post by a user.
    A post can consist of text and/or image content.
    """

    text = models.TextField(_("text"), blank=True)
    image = models.ImageField(_("image"), null=True, upload_to=get_post_image_path)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts", related_query_name="post"
    )
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ["-updated_on"]

    def __str__(self) -> str:
        return f"id: {self.id}, author: {self.author.username}"
