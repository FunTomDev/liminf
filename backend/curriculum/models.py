from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=127, unique=True)
    semester = models.ForeignKey(
        'Semester',
        on_delete=models.CASCADE,
        related_name='subjects',
        default=None
    )
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            normalized_name = unidecode(self.name).lower()
            self.slug = slugify(normalized_name)
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
            normalized_name = unidecode(self.name).lower()
            self.slug = slugify(normalized_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject} > {self.name}"

class Semester(models.Model):
    DEGREE_CHOICES = [
        ('I', 'Licencjat / Inżynier'),
    ]

    degree_type = models.CharField(
        max_length=2,
        choices=DEGREE_CHOICES,
    )
    number = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('degree_type', 'number')
        ordering = ['degree_type', 'number']

    def __str__(self):
        return f"Semestr {self.number}"