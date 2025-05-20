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

def update_problem_status(self):
    problem = self.problem

    if problem.type != 'verified':  # Only downgrade/upgrade if not verified
        helpful_exists = problem.solutions.filter(is_helpful=True).exists()
        votes_threshold = problem.solutions.filter(votes__gte=10).exists()

        if helpful_exists or votes_threshold:
            problem.type = 'solved'
        else:
            problem.type = 'unsolved'

        problem.save(update_fields=['type'])

# Create your models here.

class Solution(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='solutions')

    title = models.CharField(max_length=255, default="Rozwiązanie")
    description = models.TextField(blank=True, null=True)

    votes = models.IntegerField(default=0)
    helpful = models.BooleanField(default=False)

    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='solutions/', blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        temp_file = self.file

        # First save to generate ID
        super().save(*args, **kwargs)

        update_problem_status(self)

        if is_new and temp_file:
            # Reassign file with correct path now that ID exists
            self.file.name = solution_file_upload_path(self, os.path.basename(temp_file.name))
            if os.path.exists(temp_file.path):
                new_path = os.path.join(settings.MEDIA_ROOT, self.file.name)
                os.rename(temp_file.path, new_path)
                print("Renamed to", new_path)
            else:
                raise ValidationError(f"File {temp_file.path} does not exist.")
            super().save(update_fields=['file'])

    def __str__(self):
        return f"Solution #{self.id} for {self.problem.title}"