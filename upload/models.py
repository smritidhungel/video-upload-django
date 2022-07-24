from django.db import models
import uuid


def video_upload_path(instance, filename):
    extension = filename.split('.')[-1]
    return f"{uuid.uuid4().hex}.{extension}"


class Video(models.Model):
    video = models.FileField(upload_to=video_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
