from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from curriculum.models import Topic

import os

# Utility functions

def problem_file_upload_path(instance, filename):
    """Used to save problem files with a specific naming convention"""
    ext = filename.split('.')[-1]
    filename = f"problem_{instance.id}_{filename}"
    return os.path.join('problems', filename)


# Create your models here.

class Problem(models.Model):
    PROBLEM_TYPES = [
        ('unsolved', "Nierozwiązane"),
        ('solved', "Rozwiązane"),
        ('verified', "Sprawdzone"),
    ]

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    content = models.TextField(blank=True, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic_problems')
    type = models.CharField(max_length=16, choices=PROBLEM_TYPES, default='unsolved')

    file = models.FileField(upload_to='problems/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    @property
    def subject(self):
        return self.topic.subject
    
    def solutions(self):
        return self.solutions.all()

    def solution_count(self):
        return self.solutions.count()

    def recommended_solution(self):
        solutions = self.solutions.all()
        if not solutions.exists():
            return None
        return solutions.order_by('-likes').first()
    
    def clean(self):
        # Validate that at least one of content or file exists
        if not self.content and not self.file:
            raise ValidationError("Either content or file must be provided.")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        temp_file = self.file

        # First save to generate ID
        super().save(*args, **kwargs)

        if is_new and temp_file:
            # Reassign file with correct path now that ID exists
            self.file.name = problem_file_upload_path(self, os.path.basename(temp_file.name))
            super().save(update_fields=['file'])
    
    def get_border_style(self):
        """Returns a CSS class for the border style based on the problem type"""
        return {
            'unsolved': 'card-item__gray',
            'solved': 'card-item__green',
            'verified': 'card-item__amber'
        }.get(self.type, 'card-item__gray')


    def __str__(self):
        return f"{self.title}"