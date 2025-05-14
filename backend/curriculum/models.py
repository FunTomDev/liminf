from django.db import models
from django.utils.text import slugify

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
