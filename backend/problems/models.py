from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from curriculum.models import Topic
from django.db.models.signals import post_delete
from django.dispatch import receiver
from supabase import create_client

import posixpath
import os

# Utility functions

def problem_file_upload_path(instance, filename):
    """Used to save problem files with a specific naming convention"""
    ext = filename.split('.')[-1]
    filename = f"problem_{instance.id}_{filename}"
    return posixpath.join('problems', instance.topic.subject.slug, instance.topic.slug, filename)


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

    SEMESTER_CHOICES = [(i, f"Semestr {i}") for i in range(1, 9)]
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES, null=True, blank=True)
    
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
        is_new = self.pk is None
        temp_file = self.file

        # First save to generate ID
        super().save(*args, **kwargs)

        if is_new and temp_file:

            supabase_url = settings.SUPABASE_URL
            supabase_key = settings.SUPABASE_KEY
            supabase = create_client(supabase_url, supabase_key)

            old_path = temp_file.name
            new_path = problem_file_upload_path(self, os.path.basename(temp_file.name))

            # Download the file from Supabase
            file_data = supabase.storage.from_('uploaded.files').download(old_path)

            # Upload the file to the new path
            supabase.storage.from_('uploaded.files').upload(new_path,
                                                            file_data,
                                                            {
                                                                "content-type": "application/pdf",
                                                                "cache-control": "public, max-age=3600",
                                                                "x-amz-meta-content-disposition": "inline"  # **important**
                                                            })

            # Delete the old file
            supabase.storage.from_('uploaded.files').remove([old_path])

            # Update the file field to the new path
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