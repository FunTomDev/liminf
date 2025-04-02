from django.db import models

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=127, unique=True)

    def __str__(self):
        return self.name

def material_upload_path(instance, filename):
    """Store files in different directories based on material type."""
    if instance.material_type == 'official':
        return f"materials/official/{instance.topic.subject}/{filename}"
    elif instance.material_type == 'student_notes':
        return f"materials/student_notes/{instance.topic.subject}/{filename}"
    return f"materials/{filename}"

class Topic(models.Model):

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class Material(models.Model):
    MATERIAL_TYPES = [
        ('official', "Official Material"),
        ('student_notes', "Students' Notes"),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="materials")
    title = models.CharField(max_length=255)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES)
    description = models.CharField(max_length=2048, blank=True)
    file = models.FileField(upload_to=material_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_material_type_display()})"

class MathproArticle(models.Model):

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="mathpro_articles")
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
