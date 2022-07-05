from rest_framework import serializers

from posts.models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    """
    Fields included in create and update: `text`, `image`
    Fields included in read: all
    """

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["author", "created_on", "updated_on"]
        extra_kwargs = {"image": {"required": False}}

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """
    Fields included in create/update: `text`
    Fields included in read: all
    """

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["author", "post", "created_on", "updated_on"]

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        validated_data["post"] = self.context["post"]
        return super().create(validated_data)
