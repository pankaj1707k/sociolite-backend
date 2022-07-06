from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from users.models import FollowRelation, Profile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        ModelClass = self.Meta.model
        instance = ModelClass.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            name=validated_data["name"],
        )
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ["id", "user"]
        extra_kwargs = {
            "location": {"required": False},
            "work": {"required": False},
            "about": {"required": False},
            "date_of_birth": {"required": False},
            "picture": {"required": False},
        }


class PasswordResetSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = self.context.get("request").user
        uid = int(force_str(urlsafe_base64_decode(attrs["uid"])))

        if uid != user.id:
            detail = {"uid": "Invalid uid"}
            raise serializers.ValidationError(detail, code=401)

        if not PasswordResetTokenGenerator().check_token(user, attrs["token"]):
            detail = {"token": "Invalid token"}
            raise serializers.ValidationError(detail, code=401)

        validate_password(attrs["password"])
        return attrs

    def save(self, **kwargs):
        password = self.validated_data["password"]
        user = self.context.get("request").user
        user.set_password(password)
        user.save()
        return user


class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRelation
        fields = "__all__"
        read_only_fields = ["from_user"]

    def create(self, validated_data):
        validated_data["from_user"] = self.context["request"].user
        return super().create(validated_data)
