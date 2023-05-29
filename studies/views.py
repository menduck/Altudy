from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Study, Studying, Language, Category, Announcement
from .forms import StudyForm

# Create your views here.
def index(request):
    studies = Study.objects.all()
    
    context = {
        'studies': studies,
    }
    return render(request, 'studies/index.html', context)


def detail(request, study_pk: int):
    study = Study.objects.get(pk=study_pk)
    
    context = {
        'study': study,
    }
    return render(request, 'studies/detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = StudyForm(data=request.POST)
        if form.is_valid():
            study = form.save(commit=False)
            study.user = request.user
            study.save()
            return redirect('studies:detail', study.pk)
    else:
        form = StudyForm()
        
    context = {
        'form': form,
    }
    return render(request, 'studies/create.html', context)


def update(request, study_pk: int):
    study = Study.objects.get(pk=study_pk)
    if request.user != study.user:
        return redirect('studies:detail', study_pk)
    
    if request.method == 'POST':
        form = StudyForm(data=request.POST, instance=study)
        if form.is_valid():
            form.save()
            return redirect('studies:detail', study_pk)
    else:
        form = StudyForm(instance=study)
        
    context = {
        'study_pk': study_pk,
        'form': form,
    }
    return render(request, 'studies/update.html', context)


def delete(request, study_pk: int):
    study = Study.objects.get(pk=study_pk)
    if request.user == study.user:
        study.delete()
    
    return redirect('studies:index')