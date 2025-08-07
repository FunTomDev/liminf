from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete
from django.dispatch import receiver

from problems.models import Problem

import os
import posixpath
from supabase import create_client


# Utility functions

def solution_file_upload_path(instance, filename):
    """Used to save solution files with a specific naming convention"""
    ext = filename.split('.')[-1]
    return posixpath.join("solutions", str(instance.problem.topic.subject.slug), str(instance.problem.topic.slug), str(instance.problem.id), str(instance.id), str(filename))

def update_problem_status(self):
    problem = self.problem

    if problem.type != 'verified':  # Only downgrade/upgrade if not verified
        helpful_exists = problem.solutions.filter(helpful=True).exists()
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
    description = models.TextField(max_length=256, blank=True, null=True)

    helpful = models.BooleanField(default=False)

    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='solutions/', blank=True, null=True, max_length=600)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

        skip_file_realocation = getattr(self, 'skip_file_realocation', False)
        print("Skip file reallocation:", skip_file_realocation)

        super().save(*args, **kwargs)  # initial save

        if not skip_file_realocation and self.file:
            print(f"Saving file for problem {self.id}: {self.file.name}")
            temp_path = self.file.name
            new_path = solution_file_upload_path(self, os.path.basename(self.file.name))

            # Download the temporarily saved file
            file_data = supabase.storage.from_('uploaded.files').download(temp_path)

            # Upload to final destination
            supabase.storage.from_('uploaded.files').upload(new_path,
                                                            file_data,
                                                            {
                                                                "content-type": "application/pdf",
                                                                "cache-control": "public, max-age=3600",
                                                                "x-amz-meta-content-disposition": "inline"
                                                            })

            # Delete temporary file (Django path) from Supabase
            supabase.storage.from_('uploaded.files').remove([temp_path])

            # Update Django model with new path
            self.file.name = new_path
            super().save(update_fields=['file'])
    
    @property
    def votes_total(self):
        return self.votes.aggregate(total=models.Sum('value'))['total'] or 0

    @property
    def file_base(self):
        if self.file:
            return os.path.basename(self.file.name)
        return None

    def __str__(self):
        return f"Solution #{self.id} for {self.problem.title}"

@receiver(post_delete, sender=Solution)
def delete_file_on_material_delete(sender, instance, **kwargs):
    if instance.file:
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

        # Ensure you extract the Supabase key, not a local path or URL
        file_key = instance.file.name.replace("\\", "/")  # just in case
        
        print(f"Deleting Supabase file: {file_key}")
        
        res = supabase.storage.from_('uploaded.files').remove([file_key])

        if res == []:
            print("File does not exist or was already deleted.")
        elif res[0].get('error'):
            print(f"Error deleting file: {res[0]['error']}")

class SolutionVote(models.Model):
    """Model to track votes on solutions"""
    VOTE_CHOICES = (
        (1, 'up'),
        (-1, 'down'),
    )

    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VOTE_CHOICES, null=True)

    class Meta:
        unique_together = ('solution', 'user')

    def __str__(self):
        return f'{self.user.username} voted {self.value} on {self.solution.id}'