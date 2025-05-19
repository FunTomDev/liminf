import os
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q

from .models import Material
from curriculum.models import Subject, Topic

from .forms import MaterialForm

# Create your views here.
def materials_ajax(request):
    """Ajax materials filtering"""
    
    query = request.GET.get('q', '')
    subjects = request.GET.get('subjects', '')
    material_types = request.GET.get('types', '')
    page_number = request.GET.get('page', 1)

    topics = json.loads(request.GET.get('topics', '{}'))

    materials = Material.objects.all()
    if query:
        materials = materials.filter(title__icontains=query)
    if subjects:
        materials = materials.filter(topic__subject__slug__in=subjects.split(','))
    if topics:
        # Filter by topic IDs
        query = Q()
        for subject, topics in topics.items():
            if topics:
                query |= Q(topic__subject__slug=subject, topic__slug__in=topics)
        materials = materials.filter(query)
    if material_types:
        materials = materials.filter(type__in=material_types.split(','))

    paginator = Paginator(materials, 24)
    page_obj = paginator.get_page(page_number)

    html = render_to_string('partials/materials_list.html', {'page_obj': page_obj})
    return JsonResponse({'html': html})

def materials(request):
    """Render subjects list for materials"""

    materials_list = Material.objects.all().order_by("uploaded_at")
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

def add_material(request):
    """Add new material"""
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            material = form.save(commit=False)
            material.uploaded_by = request.user
            material.save()
            return redirect('materials:details', subject_slug=material.topic.subject.slug, topic_slug=material.topic.slug, material_id=material.id)
    else:
        form = MaterialForm()
    
    return render(request, 'materials/add_material.html', {'form': form})