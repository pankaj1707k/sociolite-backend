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
    image = models.ImageField(
        _("image"), blank=True, null=True, upload_to=get_post_image_path
    )
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
        return f"{self.id}__{self.author.username}"


class Comment(models.Model):
    """
    Model representing a comment on a post.
    A comment contains only text content and
    is related to a post and a user
    """

    text = models.TextField(_("text"))
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comment",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comment",
    )
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        ordering = ["-created_on"]

    def __str__(self) -> str:
        return f"{self.id}__{self.author.username}__{self.post.id}"


class Like(models.Model):
    """
    Model representing a like/reaction on a post.
    It does not have any content. It is related to a post and a user.
    """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes", related_query_name="like"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes", related_query_name="like"
    )
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)

    class Meta:
        verbose_name = "like"
        verbose_name_plural = "likes"
        ordering = ["-created_on"]
        constraints = [
            models.UniqueConstraint(fields=("author", "post"), name="like_author_post")
        ]

    def __str__(self) -> str:
        return f"{self.id}__{self.author.username}__{self.post.id}"
