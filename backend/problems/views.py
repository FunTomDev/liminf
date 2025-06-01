import os
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q, Prefetch, Sum, IntegerField, Value
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required

from curriculum.models import Subject, Topic, Semester
from .models import Problem
from submissions.models import Solution

from .forms import ProblemForm

# Create your views here.
def problems_ajax(request):
    """Ajax problems filtering"""

    query = request.GET.get('q', '')
    subjects = request.GET.get('subjects', '')
    problem_types = request.GET.get('types', '')
    page_number = request.GET.get('page', 1)
    semesters = request.GET.get('semesters', '')

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
    if semesters:
        problems = problems.filter(topic__subject__semester__number__in=[int(x) for x in semesters.split(',')])

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
    paginator = Paginator(problems_list, 24)  # 24 problems per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(problems_list)

    return render(request, 'problems/problems.html', context={'page_obj': page_obj, 'subjects': subjects, "semesters": Semester.objects.all()})

def details(request, subject_slug, topic_slug, problem_id):
    """Display details for a problem"""
    subject = get_object_or_404(Subject, slug=subject_slug)
    topic = get_object_or_404(Topic, slug=topic_slug, subject=subject)

    solutions_qs = Solution.objects.annotate(
        votes_value=Coalesce(Sum('votes__value'), Value(0), output_field=IntegerField())
    ).order_by('-helpful', '-votes_value', '-uploaded_at')

    problem = get_object_or_404(Problem.objects.prefetch_related(
        Prefetch(
            'solutions',
            queryset=solutions_qs.prefetch_related('votes')
        )
    ), id=problem_id, topic=topic)

    # Attach user-specific vote info to each solution (temporarily)
    for sol in problem.solutions.all():
        vote = next((v for v in sol.votes.all() if v.user_id == request.user.id), None)
        sol.user_vote_type = vote.value if vote else None
        sol.filename = os.path.basename(sol.file.name) if sol.file else None

    context = {
        'problem': problem,
        'filename': os.path.basename(problem.file.name),
    }

    return render(request, 'problems/details.html', context=context)

@login_required
def add_problem(request):
    """Add a new problem"""
    if request.method == "POST":
        form = ProblemForm(request.POST, request.FILES)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.uploaded_by = request.user
            print("Problem file is", problem.file)
            problem.save()
            return redirect('problems:details', subject_slug=problem.topic.subject.slug, topic_slug=problem.topic.slug, problem_id=problem.id)
    else:
        form = ProblemForm()

    return render(request, 'problems/add_problem.html', {'form': form})

@login_required
def edit_problem(request, problem_id):
    """Edit an existing problem"""
    problem = get_object_or_404(Problem, id=problem_id, uploaded_by=request.user)
    filename = os.path.basename(problem.file.name) if problem.file else None
    old_file = problem.file

    if request.method == 'POST':
        form = ProblemForm(request.POST, request.FILES, instance=problem)
        if form.is_valid():
            # File delete logic (only if the user has uploaded a new file or requested to clear the file)
            if form.cleaned_data.get('clear_file') or 'file' in request.FILES:
                print("Clearing old file for problem:", problem_id)
                if old_file:
                    old_file.delete(save=False)
                    problem.file = None if not 'file' in request.FILES else request.FILES['file']

            form.save()
            return redirect('users:profile')
    else:
        print("Editing problem with ID:", problem_id, problem)
        form = ProblemForm(instance=problem)

    return render(request, 'problems/edit_problem.html', {'form': form, 'problem': problem, 'filename': filename})

@login_required
def delete_problem(request, problem_id):
    """Delete a problem"""
    problem = get_object_or_404(Problem, id=problem_id)
    if request.method == 'POST':
        if problem.uploaded_by == request.user:
            problem.delete()
            return redirect('users:profile')
        else:
            return JsonResponse({'status': 'error', 'message': 'No permission'}, status=403)

    return render(request, 'problems/delete_problem.html', {'problem': problem})