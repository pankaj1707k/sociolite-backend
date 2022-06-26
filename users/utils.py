from rest_framework_simplejwt.tokens import RefreshToken


def get_token_pair(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


def get_profile_image_path(instance, filename) -> str:
    ext = filename.split(".")[-1]  # extract file extension
    return f"profile/{instance.user.username}.{ext}"
