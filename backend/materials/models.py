from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from curriculum.models import Topic

import os

# Specify the upload path for materials based on their type
def material_upload_path(instance, filename)->str:
    """Store files in different directories based on material type."""
    if instance.material_type == 'official':
        return f"materials/official/{instance.topic.subject}/{filename}"
    elif instance.material_type == 'student_notes':
        return f"materials/student_notes/{instance.topic.subject}/{filename}"
    return f"materials/{filename}"

# Create your models here.
class Material(models.Model):
    MATERIAL_TYPES = [
        ('official', "Oficjalne"),
        ('student_notes', "Notatki"),
        ('article', "Artykuł"),
    ]

    # Relations and metadata
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="materials")
    title = models.CharField(max_length=255)

    SEMESTER_CHOICES = [(i, f"Semestr {i}") for i in range(1, 9)]
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES, null=True, blank=True)
    
    type = models.CharField(max_length=20, choices=MATERIAL_TYPES, default='student_notes')

    # Material content
    description = models.CharField(max_length=2048, blank=True)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to=material_upload_path, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.title}"

    def clean(self):
        if self.type == "article":
            if not self.url:
                raise ValidationError("Artykuły muszą mieć link URL.")
            if self.file:
                raise ValidationError("Artykuły nie mogą mieć załączonego pliku.")
        if self.type != "article" and not self.file and not self.content:
            print(_("Materials must have content or file."))
            raise ValidationError("Materiały muszą mieć treść albo załączony plik.")
        super().clean()

    def get_border_style(self):
        return {
            'student_notes': 'card-item__sky',
            'article': 'card-item__violet',
            'official': 'card-item__gray'
        }.get(self.type, 'card-item__gray')

@receiver(post_delete, sender=Material)
def delete_file_on_material_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
