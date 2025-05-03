import os
import json

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q

from curriculum.models import Subject, Topic
from .models import Problem

# Create your views here.
def problems_ajax(request):
    """Ajax problems filtering"""

    query = request.GET.get('q', '')
    subjects = request.GET.get('subjects', '')
    problem_types = request.GET.get('types', '')
    page_number = request.GET.get('page', 1)

    topics = json.loads(request.GET.get('topics', '{}'))

    problems = Problem.objects.all()
    if query:
        problems = problems.filter(title__icontains=query)
    if subjects:
        problems = problems.filter(topic__subject__slug__in=subjects.split(','))
    if topics:
        # Filter by topic IDs
        query = Q()
        for subject, topics in topics.items():
            if topics:
                query |= Q(topic__subject__slug=subject, topic__slug__in=topics)
        problems = problems.filter(query)
    if problem_types:
        problems = problems.filter(type__in=problem_types.split(','))

    paginator = Paginator(problems, 24)
    page_obj = paginator.get_page(page_number)

    html = render_to_string('partials/problems_list.html', {'page_obj': page_obj})
    return JsonResponse({'html': html})

def problems(request):
    """View the list of all published problems"""

    problems_list = Problem.objects.all().order_by("uploaded_at")
    subjects = {}
    for topic in Topic.objects.select_related('subject'):
        if topic.subject not in subjects:
            subjects[topic.subject] = []
        subjects[topic.subject].append(topic)
    paginator = Paginator(problems_list, 24)  # 24 materials per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'submissions/problems.html', context={'page_obj': page_obj, 'subjects': subjects})

def details(request, subject_slug, topic_slug, material_id):
    """Display details material"""
    subject = get_object_or_404(Subject, slug=subject_slug)
    topic = get_object_or_404(Topic, slug=topic_slug, subject=subject)
    problem = get_object_or_404(Problem, id=material_id, topic=topic)

    context = {
        'material': problem,
        'file_name': os.path.basename(problem.file.name),
    }

    return render(request, 'problems/details.html', context=context)

def solution(request, problem_id):
	"""View solution for given problem"""
	return render(request, 'submissions/solution.html')
