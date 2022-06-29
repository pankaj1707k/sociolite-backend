import uuid


def get_post_image_path(instance, filename):
    ext = filename.split(".")[-1]  # extract file extension
    return f"post/{instance.author.username}/{uuid.uuid4().hex}.{ext}"
