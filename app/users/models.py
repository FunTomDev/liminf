from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """
    
    STUDENT = 'student'
    CONTRIBUTOR = 'contributor'
    EDITOR = 'editor'
    ADMIN = 'admin'

    ACCOUNT_TYPE_CHOICES = [
        (STUDENT, 'Student'),
        (CONTRIBUTOR, 'Contributor'),
        (EDITOR, 'Editor'),
        (ADMIN, 'Admin'),
    ]

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        default=STUDENT
    )

    bio = models.TextField(blank=True)

    # Boolean flags for permissions
    can_upload_notes = models.BooleanField(default=True)
    can_upload_problems = models.BooleanField(default=True)
    can_upload_solutions = models.BooleanField(default=True)
    can_upload_official = models.BooleanField(default=False)


    def __str__(self):
        return self.username
