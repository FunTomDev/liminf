from django.db import models
from django.contrib.auth.models import AbstractUser
import morfeusz2

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

    @property
    def voc_name(self):
        """
        Returns the vocname of the user.
        If the user has a first name, it returns the first name.
        Otherwise, it returns the username.
        """
        morf = morfeusz2.Morfeusz()
        if not self.first_name:
            return self.username
        analyses = morf.generate(self.first_name)
        for form, base, tags, _, _ in analyses:
            if ':voc:' in tags:
                return form
        # fallback if no vocative form found
        return self.first_name

    bio = models.TextField(blank=True)

    # Boolean flags for permissions
    can_upload_notes = models.BooleanField(default=True)
    can_upload_problems = models.BooleanField(default=True)
    can_upload_solutions = models.BooleanField(default=True)
    can_upload_official = models.BooleanField(default=False)


    def __str__(self):
        return self.username

class Semester(models.Model):
    name = models.CharField(max_length=50, unique=True)
    position = models.PositiveSmallIntegerField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['position']
