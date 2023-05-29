from django.shortcuts import render, get_object_or_404

from .models import Problem

# Create your views here.
def detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    context = {
        'problem': problem
    }
    return render(request, 'studies/detail.html', context)