import json

from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view
from taggit.models import Tag

from studies.models import Study
from .forms import ProblemForm, ReviewForm, CommentForm
from .models import Problem, Review, Comment

'''다른 스터디 선택하기 기능이 추가되어야 한다'''
# Create your views here.
@login_required
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


@login_required
def create(request):
    if 'study_id' not in request.session:
        return redirect('studies:mainboard')

    study_id = request.session.get('study_id')
    
    if request.method == 'POST':
        form = ProblemForm(data=request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.user, problem.study = request.user, get_object_or_404(Study, pk=study_id)
            problem.save()
            form.save_m2m()
            return redirect('reviews:detail', problem.pk)

        return redirect('studies:mainboard')
    else:
        form = ProblemForm()
    context = {
        'form': form,
        # 'study_id': study_id,
    }
    return render(request, 'reviews/create.html', context)


@login_required
def update(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.user != problem.user:
        return redirect('reviews:detail', problem.pk)
    
    if request.method == 'POST':
        form = ProblemForm(data=request.POST, instance=problem)
        if form.is_valid():
            form.save_m2m()
            form.save()
            return redirect('reviews:detail', problem.pk)
    else:
        form = ProblemForm(instance=problem)
    context = {
        'form': form,
    }
    return render(request, 'reviews/update.html', context)


@login_required
def delete(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.user == problem.user:
        try:
            problem.delete()
            return redirect('studies:mainboard')
        finally:
            # 레이스 컨디션 테스트 어떻게?
            Tag.objects.annotate(ntag=Count('taggit_taggeditem_items')).filter(ntag=0).delete()
    # 권한이 없는 페이지 만들기?
    # 왔던 곳으로 되돌아가게 하려면?
    return redirect('reviews:detail', pk)
    

@login_required
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


@login_required
def review_update(request, review_pk):
    review = get_object_or_404(Review.objects.select_related('problem'), pk=review_pk)
    if request.user != review.user:
        return redirect('reviews:detail', review.problem.pk)
    
    if request.method == 'POST':
        form = ReviewForm(data=request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews:detail', review.problem.pk)
    else:
        form = ReviewForm(instance=review)
    context = {
        'form': form,
    }
    return render(request, 'reviews/review_update.html', context)


@login_required
def review_delete(request, review_pk):
    review = get_object_or_404(Review.objects.select_related('problem'), pk=review_pk)
    if request.user == review.user:
        try:
            review.delete()
            return redirect('studies:index')
        finally:
            Tag.objects.annotate(ntag=Count('taggit_taggeditem_items')).filter(ntag=0).delete()
    return redirect('reviews:detail', review.problem.pk)


@login_required
def comment_create(request, review_pk):
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            review = get_object_or_404(Review.objects.select_related('problem'), pk=review_pk)
            comment.user, comment.review = request.user, review
            comment.save()
            return redirect('reviews:detail', review.problem.pk)
    else:
        form = CommentForm()
    context = {
        'form': form,
    }
    return render(request, 'reviews/comment_create.html', context)


@login_required
def comment_update(request, comment_pk):
    comment = get_object_or_404(Comment.objects.select_related('review__problem'), pk=comment_pk)
    if request.user != comment.user:
        return redirect('reviews:detail', comment.review.problem.pk)
    
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews:detail', comment.review.problem.pk)
    else:
        form = CommentForm()
    context = {
        'form': form,
    }
    return render(request, 'reviews/comment_create.html', context)


@login_required
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment.objects.select_related('review__problem'), pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('reviews:detail', comment.review.problem.pk)

    
@login_required
def like(request):
    try:
        data = json.loads(request.body)
        object_identifier = data.get('objectIdentifier')
        if object_identifier is not None:
            model, pk = object_identifier.split('-')
            obj = get_object_or_404(eval(model), pk=pk)
    except:
        raise Http404("Request not valid")

    # 조건문 추가해 Problem, Review, Comment 별로 swap_text 수정 가능
    if request.user in obj.like_users.all():
        obj.like_users.remove(request.user)
        response = {
            'swap_text': '좋아요',
        }
    else:
        obj.like_users.add(request.user)
        response = {
            'swap_text': '좋아요 취소',
        }
    return JsonResponse(response)
        
    