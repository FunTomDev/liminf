import os
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string

from problems.models import Problem
from .models import Solution, SolutionVote

from .forms import SolutionForm

# Create your views here.
@require_POST
@login_required
def vote_solution_ajax(request, subject_slug, topic_slug, problem_id, solution_id):

    vote_type = request.POST.get('vote_type')
    if vote_type not in ['up', 'down']:
        return JsonResponse({'status': 'error', 'message': 'Invalid vote type'}, status=400)

    solution = get_object_or_404(Solution, id=solution_id)
    value = 1 if vote_type == 'up' else -1

    vote, created = SolutionVote.objects.get_or_create(user=request.user, solution=solution)

    if not created and vote.value == value:
        # Same vote clicked again → remove vote
        vote_type = None
        vote.delete()
    else:
        # Update or set vote
        vote.value = value
        vote.save()

    # Return updated total
    total_votes = solution.votes_total or 0

    return JsonResponse({'status': 'ok', 'total_votes': total_votes, 'vote_type': vote_type})

def ajax_solution_detail(request, subject_slug, topic_slug, problem_id, solution_id):
    try:
        solution = Solution.objects.get(id=solution_id)
        vote = next((v for v in solution.votes.all() if v.user_id == request.user.id), None)
        solution.user_vote_type = vote.value if vote else None
        print("User vote type:", solution.user_vote_type)
        filename = os.path.basename(solution.file.name)
    except Solution.DoesNotExist:
        raise Http404("Solution not found")

    html = render_to_string('partials/solution_details_partial.html', {'solution': solution, 'filename': filename, 'user': request.user})
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

@login_required
def edit_solution(request, subject_slug, topic_slug, problem_id, solution_id):
    solution = get_object_or_404(Solution, id=solution_id, uploaded_by=request.user)
    filename = os.path.basename(solution.file.name) if solution.file else None
    old_file = solution.file
    solution.skip_file_realocation = False # ensure file realocation

    if request.method == 'POST':
        form = SolutionForm(request.POST, request.FILES, instance=solution)
        if form.is_valid():
            # File delete logic (only if the user has uploaded a new file or requested to clear the file)
            if form.cleaned_data.get('clear_file') or 'file' in request.FILES:
                print("Clearing old file for solution:", solution_id)
                if old_file:
                    old_file.delete(save=False)
                    solution.file = None if not 'file' in request.FILES else request.FILES['file']
            else:
                 # File is not cleared nor new file was uploaded
                print("Keeping old file for solution:", solution_id)
                solution.skip_file_realocation = True
            form.save()
            return redirect('users:profile')
    else:
        print("Editing solution with ID:", solution_id, solution)
        form = SolutionForm(instance=solution)

    return render(request, 'submissions/edit_solution.html', {'form': form, 'solution': solution, 'filename': filename})

@login_required
def delete_solution(request, subject_slug, topic_slug, problem_id, solution_id):
    """Delete a solution"""
    solution = get_object_or_404(Solution, id=solution_id)
    if request.method == 'POST':
        if solution.uploaded_by == request.user:
            solution.delete()
            return redirect('users:profile')
        else:
            return JsonResponse({'status': 'error', 'message': 'No permission'}, status=403)
    return render(request, 'submissions/delete_solution.html', {'solution': solution})
