from django.db import models
from django.conf import settings
from materials.models import Topic

# Create your models here.

class Problem(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    content = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic_problems')

    file = models.FileField(upload_to='problems/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    @property
    def subject(self):
        return self.topic.subject

    #TODO: Add file is null verification if content is null

    def __str__(self):
        return f"{self.title}"

class Solution(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='problem_solutions')

    content = models.TextField()
    file = models.FileField(upload_to='solutions/', blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Solution #{self.id} for {self.problem.title}"