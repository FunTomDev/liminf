import os
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from problems.models import Problem
from .models import Solution

from .forms import SolutionForm

# Create your views here.
def ajax_solution_detail(request, subject_slug, topic_slug, problem_id, solution_id):
    try:
        solution = Solution.objects.get(id=solution_id)
        filename = os.path.basename(solution.file.name)
    except Solution.DoesNotExist:
        raise Http404("Solution not found")

    html = render_to_string('partials/solution_details_partial.html', {'solution': solution, 'filename': filename})
    return JsonResponse({'html': html})

@login_required
def toggle_helpful_solution(request, subject_slug, topic_slug, problem_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

    solution_id = request.POST.get('solution_id')
    try:
        solution = Solution.objects.select_related('problem').get(id=solution_id)
        if solution.problem.uploaded_by != request.user:
            return JsonResponse({'status': 'error', 'message': 'No permission'}, status=403)

        solution.helpful = not solution.helpful
        solution.save()
        return JsonResponse({'status': 'ok', 'helpful': solution.helpful})
    except Solution.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Solution not found'}, status=404)

def solution(request, problem_id):
	"""View solution for given problem"""
	return render(request, 'submissions/solution.html')

@login_required
def add_solution(request, subject_slug, topic_slug, problem_id):
	"""Add a solution to a problem"""
	problem = get_object_or_404(Problem, id=problem_id)
	if request.method == 'POST':
		form = SolutionForm(request.POST, request.FILES)
		if form.is_valid():
			solution = form.save(commit=False)
			solution.problem = problem
			solution.uploaded_by = request.user
			solution.save()
			return redirect('problems:details', subject_slug=problem.topic.subject.slug, topic_slug=problem.topic.slug, problem_id=problem.id)
	else:
		form = SolutionForm()
	return render(request, 'submissions/add_solution.html', {'form': form, 'problem': problem})
