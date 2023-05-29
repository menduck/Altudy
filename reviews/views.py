from django.shortcuts import render, get_object_or_404, redirect

from .forms import ProblemForm
from .models import Problem


# Create your views here.
def detail(request, pk):
    problem = get_object_or_404(
        Problem.objects.prefetch_related(
            'tags',
            'review_set__tags',
            'review_set__comment_set__tags',
        ),
        pk=pk
    )
    # problem = get_object_or_404(
    #     Problem, pk=pk
    # )
    context = {
        'problem': problem,
    }
    return render(request, 'reviews/detail.html', context)


def create(request):
    if request.method == 'POST':
        form = ProblemForm(data=request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.user = request.user
            problem.save()
            return redirect('reviews:detail', problem.pk)
    else:
        form = ProblemForm()
    context = {
        'form': form,
    }
    return render(request, 'reviews/create.html', context)