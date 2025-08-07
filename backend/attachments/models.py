from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.exceptions import ValidationError
import os

# Utility functions

def attachment_upload_to(instance, filename):
    """Save attachments into media/{app_label}/{model_name}/{id}/{filename}"""
    app_label = instance.content_type.app_label
    model_name = instance.content_type.model
    obj_id = instance.object_id
    return f"{app_label}/{model_name}/{obj_id}/{filename}"

def validate_file_extension(value):
    """Optional: validate allowed file types."""
    ext = os.path.splitext(value.name)[1].lower()
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
    if ext not in allowed_extensions:
        raise ValidationError(f"Unsupported file extension: {ext}")

# Create your models here.

class Attachment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    file = models.FileField(upload_to=attachment_upload_to, validators=[validate_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Attachment for {self.content_type} {self.object_id}"