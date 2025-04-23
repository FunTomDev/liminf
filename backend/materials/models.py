from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.core.exceptions import ValidationError

import os

# Signal to delete file from filesystem when Material is deleted

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=127, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

def material_upload_path(instance, filename):
    """Store files in different directories based on material type."""
    if instance.material_type == 'official':
        return f"materials/official/{instance.topic.subject}/{filename}"
    elif instance.material_type == 'student_notes':
        return f"materials/student_notes/{instance.topic.subject}/{filename}"
    return f"materials/{filename}"

class Topic(models.Model):

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['subject', 'slug'], name='unique_topic_slug_per_subject')
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject} > {self.name}"
    
class Material(models.Model):
    MATERIAL_TYPES = [
        ('official', "Oficjalne"),
        ('student_notes', "Notatki"),
        ('mathpro', "MathPro"),
    ]

    # Relations and metadata
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="materials")
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=MATERIAL_TYPES)

    # Material content
    short_description = models.CharField(max_length=2048, blank=True)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to=material_upload_path, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.title}"
    
    def clean(self):
        if self.type == "mathpro":
            if not self.url:
                raise ValidationError("MathPro articles must have a URL.")
            if self.file:
                raise ValidationError("MathPro articles cannot have a file.")
        if self.type != "mathpro" and not self.file and not self.content:
            raise ValidationError("Materials must have content or file.")
        super().clean()

    def get_border_style(self):
        return {
            'student_notes': 'material-item__orange',
            'mathpro': 'material-item__lime',
            'official': 'material-item__gray'
        }.get(self.type, 'material-item__gray')

@receiver(post_delete, sender=Material)
def delete_file_on_material_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
