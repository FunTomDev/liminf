from django.db import models

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

class ProblemSet(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='problem_sets')

    def __str__(self):
        return f"{self.topic.name} - {self.title}"

class Problem(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.title}"

class Solution(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='problem_solutions')

    description = models.CharField(max_length=2048)

    def __str__(self):
        return f"Solution for {self.problem.title}"