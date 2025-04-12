import os
from django.shortcuts import render, get_object_or_404
from .models import Subject, Topic, Material
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

# Create your views here.
def materials_ajax(request):
    query = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    materials = Material.objects.all()
    if query:
        materials = materials.filter(title__icontains=query)

    paginator = Paginator(materials, 24)
    page_obj = paginator.get_page(page_number)

    html = render_to_string('partials/materials_list.html', {'page_obj': page_obj})
    return JsonResponse({'html': html})

def materials(request):
    """Render subjects list for materials"""

    materials_list = Material.objects.all()
    subjects = {}
    for topic in Topic.objects.select_related('subject'):
        if topic.subject not in subjects:
            subjects[topic.subject] = []
        subjects[topic.subject].append(topic)
    paginator = Paginator(materials_list, 24)  # 24 materials per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'materials/materials.html', context={'page_obj': page_obj, 'subjects': subjects})


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