from django.urls import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q, Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from taggit.models import Tag, TaggedItem

from studies.models import Study
from .forms import ProblemForm, ReviewForm
from .models import Problem, Review
from .utils import OrderedCounter


# def user_has_access_to_study(request):
#     user = request.user
#     study = eval(f'get_object_or_404(Study, request.{request.method}.get("study"))')



# Create your views here.
def index(request):
    # print(request.session.__dir__())
    study_id = request.GET.get('study')   # 세션에 저장, 로그인시 어떻게 유지?
    study = get_object_or_404(Study, pk=study_id)
    problems = Problem.objects.filter(study=study).order_by('-post_num')
    context = {
        'problems': problems,
    }
    return render(request, 'reviews/index.html', context)


def detail(request, pk):
    problem = get_object_or_404(
        Problem.objects.prefetch_related(
            'tags',
            'review_set__tags',
            'review_set__comment_set__tags',
        ),
        pk=pk
    )
    context = {
        'problem': problem,
    }
    return render(request, 'reviews/detail.html', context)


def create(request):
    if request.method == 'POST':
        study_id = request.POST.get('study')
        form = ProblemForm(data=request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.user = request.user
            problem.study = get_object_or_404(Study, pk=study_id)
            problem.save()
            form.save_m2m()
            url = reverse_lazy('reviews:detail', kwargs={'pk': problem.pk}) + f'?study={study_id}'
            return redirect(url)
        return redirect('/')
    else:
        form = ProblemForm()
    context = {
        'form': form,
        'study_id': request.GET.get('study'),
    }
    return render(request, 'reviews/create.html', context)


def update(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.method == 'POST':
        form = ProblemForm(data=request.POST, instance=problem)
        if form.is_valid():
            form.save_m2m()
            form.save()
            return redirect('reviews:detail', problem.pk)
        print('not valid')
    else:
        form = ProblemForm(instance=problem)
    context = {
        'form': form,
    }
    return render(request, 'reviews/update.html', context)


def delete(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.user == problem.user:
        try:
            problem.delete()
            return redirect('/')
        finally:
            Tag.objects.annotate(ntag=Count('taggit_taggeditem_items')).filter(ntag=0).delete()
    # 권한이 없는 페이지 만들기?
    # 왔던 곳으로 되돌아가게 하려면?
    return redirect('reviews:detail', pk)
    

def review_create(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user, review.problem = request.user, problem
            review.save()
            return redirect('reviews:detail', problem.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
        'problem_pk': pk,
    }
    return render(request, 'reviews/review_create.html', context)


def review_update(request, pk, review_pk):
    problem = get_object_or_404(Problem, pk=pk)
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        form = ReviewForm(data=request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews:detail', problem.pk)
    else:
        form = ReviewForm(instance=review)
    context = {
        'form': form,
    }
    return render(request, 'reviews/review_update.html', context)


def review_delete(request, pk, review_pk):
    review = get_object_or_404(Review.objects.select_related('problem'), pk=review_pk)
    if request.user == review.user:
        try:
            review.delete()
            return redirect('/')
        finally:
            Tag.objects.annotate(ntag=Count('taggit_taggeditem_items')).filter(ntag=0).delete()
    return redirect('reviews:detail', pk)