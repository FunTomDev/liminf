from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import TopicForm, SubjectForm

# Create your views here.
@login_required
def add_topic(request):
    next_url = request.GET.get('next') or request.POST.get('next') or reverse('home')
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next_url)
    else:
        form = TopicForm()
    return render(request, 'curriculum/add_topic.html', {'form': form, 'next': next_url, 'request': request})

@login_required
def add_subject(request):
    next_url = request.GET.get('next') or request.POST.get('next') or reverse('home')
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next_url)
    else:
        form = SubjectForm()
    return render(request, 'curriculum/add_subject.html', {'form': form, 'next': next_url, 'request': request})