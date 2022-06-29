from django.contrib import admin

from posts.models import Comment, Like, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post")
