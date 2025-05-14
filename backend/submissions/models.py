from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from problems.models import Problem

import os


# Utility functions

def solution_file_upload_path(instance, filename):
    """Used to save solution files with a specific naming convention"""
    ext = filename.split('.')[-1]
    filename = f"solution_{instance.id}_{filename}"
    return os.path.join('solutions', filename)

# Create your models here.

class Solution(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='solutions')

    votes = models.IntegerField(default=0)

    content = models.TextField()
    file = models.FileField(upload_to='solutions/', blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

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
            self.file.name = solution_file_upload_path(self, os.path.basename(temp_file.name))
            super().save(update_fields=['file'])

    def __str__(self):
        return f"Solution #{self.id} for {self.problem.title}"