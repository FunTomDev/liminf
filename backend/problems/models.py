from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from curriculum.models import Topic
from django.db.models.signals import post_delete
from django.dispatch import receiver
from supabase import create_client

import posixpath
import os

from curriculum.models import Semester

# Utility functions

def problem_file_upload_path(instance, filename):
    """Used to save problem files with a specific naming convention"""
    ext = filename.split('.')[-1]
    return posixpath.join("problems", str(instance.topic.subject.slug), str(instance.topic.slug), str(instance.id), str(filename))


# Create your models here.

class Problem(models.Model):
    PROBLEM_TYPES = [
        ('unsolved', "Nierozwiązane"),
        ('solved', "Rozwiązane"),
        ('verified', "Sprawdzone"),
    ]

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic_problems')

    semester = models.ForeignKey(
        Semester,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Semestr',
        related_name='problems'
    )
    
    type = models.CharField(max_length=16, choices=PROBLEM_TYPES, default='unsolved')

    file = models.FileField(upload_to="problems/", blank=True, null=True, max_length=600)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    @property
    def subject(self):
        return self.topic.subject

    def solution_count(self):
        return self.solutions.count()

    def recommended_solution(self):
        solutions = self.solutions.all()
        if not solutions.exists():
            return None
        return solutions.order_by('-votes').first()
    
    def get_border_style(self):
        """Returns a CSS class for the border style based on the problem type"""
        return {
            'unsolved': 'card-item__gray',
            'solved': 'card-item__green',
            'verified': 'card-item__amber'
        }.get(self.type, 'card-item__gray')
    
    def save(self, *args, **kwargs):
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

        skip_file_realocation = getattr(self, 'skip_file_realocation', False)
        print("Skip file reallocation:", skip_file_realocation)

        super().save(*args, **kwargs)  # initial save

        if not skip_file_realocation and self.file:
            print(f"Saving file for problem {self.id}: {self.file.name}")
            temp_path = self.file.name
            new_path = problem_file_upload_path(self, os.path.basename(self.file.name))

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


    def __str__(self):
        return f"{self.title}"

@receiver(post_delete, sender=Problem)
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