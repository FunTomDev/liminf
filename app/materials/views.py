import os
from django.shortcuts import render, get_object_or_404
from .models import Subject, Topic, Material

# Create your views here.
def materials(request):
    """Render subjects list for materials"""
    return render(request, "materials/materials.html")


def details(request, subject_slug, topic_slug, material_id):
    """Display details material"""
    subject = get_object_or_404(Subject, slug=subject_slug)
    topic = get_object_or_404(Topic, slug=topic_slug, subject=subject)
    material = get_object_or_404(Material, id=material_id, topic=topic)

    context = {
        'material': material,
        'file_name': os.path.basename(material.file.name),
    }

    return render(request, 'materials/details.html', context=context)