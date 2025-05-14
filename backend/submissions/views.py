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
def solution(request, problem_id):
	"""View solution for given problem"""
	return render(request, 'submissions/solution.html')
