import json
import operator
import logging
from functools import reduce
from typing import Any

from django.http import JsonResponse, Http404, QueryDict
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Prefetch
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.db import transaction

from taggit.models import Tag

from .forms import ProblemForm, ReviewForm, CommentForm
from .models import Problem, Review, Comment
from .utils import render, HttpResponse, HTTPResponseHXRedirect

from studies.models import Study


# 로깅 설정
logger = logging.getLogger(__name__)


# Create your views here.
@login_required
def detail(request, pk):
    '''
    42 queries in 14.26ms → 31 queries in 13.03ms
    '''
    problem = get_object_or_404(
        Problem.objects.prefetch_related(
            'tags',
            Prefetch(
                'review_set', 
                queryset=Review.objects.prefetch_related(
                    'tags',
                    Prefetch(
                        'comment_set',
                        queryset=Comment.objects.select_related('user').prefetch_related('like_users'),
                    ),
                ).select_related('user').prefetch_related('like_users'),
            ),
        ).select_related('study', 'user'),
        pk=pk
    )

    if not problem.study.studying_users.filter(username=request.user).exists():
        return redirect('studies:detail', problem.study.pk)
    
    querydict = {
        'problem': Q(problem_set=pk),
        'review': Q(review_set__in=problem.review_set.values('id')),
    }

    tags = Tag.objects.filter(reduce(operator.__or__, querydict.values()))
    tags = tags.annotate(freq=Count('name'))
    ordered_tags = tags.order_by('-freq').values('name')

    context = {
        'problem': problem,
        'tags': ordered_tags.values(),
        'study' : problem.study
    }
    return render(request, 'reviews/detail.html', context)


@require_http_methods(['GET', 'POST'])
@login_required
def create(request):
    study_id = request.GET.get('study', request.session.get('study_id'))
    member = get_object_or_404(
        Study, pk=study_id,
    ).studying_users.filter(username=request.user).exists()
    
    if study_id is None or not member:
        return redirect('studies:detail', study_id)
    
    request.session['study_id'] = study_id
    
    if request.method == 'POST':
        form = ProblemForm(data=request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.user, problem.study = request.user, get_object_or_404(Study, pk=study_id)
            problem.save()
            form.save_m2m()
            return redirect('reviews:detail', problem.pk)

        return redirect('studies:mainboard', study_id)
    else:
        form = ProblemForm()
    context = {
        'form': form,
    }
    return render(request, 'reviews/create.html', context)


@require_http_methods(['GET', 'PUT'])
@login_required
def update(request, pk):
    problem = get_object_or_404(Problem.objects.select_related('study'), pk=pk)
    
    if request.user != problem.user:
        return HTTPResponseHXRedirect(redirect_to=reverse_lazy('reviews:detail', kwargs={'pk': pk}))
    
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = ProblemForm(data, instance=problem)
        if form.is_valid():
            updated_form = form.save(commit=False)
            updated_form.save()
            form.save_m2m()
            return HTTPResponseHXRedirect(redirect_to=reverse_lazy('reviews:detail', kwargs={'pk': pk}))
    else:
        form = ProblemForm(instance=problem)
    context = {
        'form': form,
    }
    return render(request, 'reviews/update.html', context)


@require_http_methods(['DELETE'])
@login_required
def delete(request, pk):
    problem = get_object_or_404(
        Problem.objects.select_related('study'), pk=pk,
    )
    study_pk = problem.study.pk

    if request.user == problem.user:
        problem.delete()
        return HTTPResponseHXRedirect(redirect_to=reverse_lazy('studies:mainboard', kwargs={'study_pk':study_pk}))
    return HTTPResponseHXRedirect(redirect_to=reverse_lazy('reviews:detail', kwargs={'pk': pk}))
    

@require_http_methods(['GET', 'POST'])
@login_required
def review_create(request, pk):
    problem = get_object_or_404(
        Problem.objects.select_related('study'),
        pk=pk,
    )
    
    if not problem.study.studying_users.filter(username=request.user).exists():
        return redirect('studies:detail', problem.study.pk)
    
    if request.method == 'POST':
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user, review.problem = request.user, problem
            review.save()
            form.save_m2m() 

            # 유저의 experience를 10 증가시킴
            with transaction.atomic():
                user = request.user
                user.experience += 10
                user.save()


            context = {
                'problem': Problem.objects.get(pk=pk)
            }
            return redirect('reviews:detail', review.problem.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
        'problem_pk': pk,
    }
    return render(request, 'reviews/review_create.html', context)


@require_http_methods(['GET', 'PUT'])
@login_required
def review_update(request, review_pk):
    review = get_object_or_404(
        Review.objects.select_related('problem__study'),
        pk=review_pk,
    )
    study_pk = review.problem.study.pk
    if not review.problem.study.studying_users.filter(username=request.user).exists():
        return HTTPResponseHXRedirect(redirect_to=reverse_lazy('studies:detail', kwargs={'study_pk': study_pk}))
    
    if request.user != review.user:
        return HTTPResponseHXRedirect(redirect_to=reverse_lazy('reviews:detail', kwargs={'pk': review.problem.pk}))
    
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = ReviewForm(data, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            form.save_m2m()
            return HTTPResponseHXRedirect(redirect_to=reverse_lazy('reviews:detail', kwargs={'pk': review.problem.pk}))
    else:
        form = ReviewForm(instance=review)
    context = {
        'form': form,
    }
    return render(request, 'reviews/review_update.html', context)


@require_http_methods(['DELETE'])
@login_required
def review_delete(request, review_pk):
    review = get_object_or_404(
        Review.objects.select_related('problem__study'),
        pk=review_pk
    )
    problem_pk = review.problem.pk
    if request.user == review.user:
        review.delete()
        messages.add_message(request, messages.SUCCESS, "리뷰가 성공적으로 삭제되었습니다.")
    return HTTPResponseHXRedirect(redirect_to=reverse_lazy('reviews:detail', kwargs={'pk': problem_pk}))


@require_http_methods(['GET', 'POST'])
@login_required
def comment_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user, comment.review = request.user, review
            comment.save()

            # 작성한 유저에게 5의 경험치 추가
            comment.user.experience += 5
            comment.user.save()
            context = {
                'review': Review.objects.prefetch_related('comment_set__user').get(pk=review_pk),
            }
            trigger = json.dumps({
                'clear-textarea': {
                    'textarea_id': f'comment-textarea-{review.pk}',
                }, 
                'recount': {
                    'counter_id': f'comment-count-Review-{review.pk}',
                    'count': review.comment_set.count(),
                }
            })
            return render(request, 'reviews/comments/list.html', context, trigger=trigger)
        return render(request, 'reviews/comments/list.html', context)
    else:
        form = CommentForm()
    context = {
        'comment_form': form,
        'review': review,
    }
    return render(request, 'reviews/comments/create.html', context)


@require_http_methods(['GET', 'PUT'])
@login_required
def comment_update(request, comment_pk):
    comment = get_object_or_404(
        Comment.objects.select_related('review'),
        pk=comment_pk
    )
    context = {
        'comment': comment,
        'review': comment.review,
    }    
    if request.user != comment.user:
        return render(request, 'reviews/comments/item.html', context)
    
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = CommentForm(data=data, instance=comment)
        if form.is_valid():
            form.save()
            return render(request, 'reviews/comments/item.html', context)
        context['comment_form'] = form
        return render(request, 'reviews/comments/list.html', context)
    else:
        context['comment_form'] = CommentForm(instance=comment)
    return render(request, 'reviews/comments/update.html', context)


@require_http_methods(['DELETE'])
@login_required
def comment_delete(request, comment_pk):
    comment = get_object_or_404(
        Comment.objects.select_related('review'),
        pk=comment_pk
    )
    review = comment.review
    context = {
        'review': review
    }
    if request.user == comment.user:
        comment.delete()
        trigger = json.dumps({
            'recount': {
                'counter_id': f'comment-count-Review-{review.pk}',
                'count': review.comment_set.count(),
            }
        })
        return HttpResponse(trigger=trigger)
    
    return render(request, 'reviews/comments/item.html', context)


@login_required
def like(request):
    try:
        object_identifier = json.loads(request.body).get('objectIdentifier')
    except:
        raise Http404("Request not valid")
    
    if object_identifier is not None:
        model, pk = object_identifier.split('-')
        if model not in {'Problem', 'Review', 'Comment'}:
            raise Http404("Request not valid")
        obj = get_object_or_404(eval(model), pk=pk)
    else:
        raise Http404("Request not valid")


    if request.user in obj.like_users.all():
        obj.like_users.remove(request.user)
        context = {
            'liked': False
        }
        if model == 'Review':
            # 좋아요 취소 시 받은 경험치 되돌림
            obj.user.experience -= 10
            obj.user.save()
    else:
        obj.like_users.add(request.user)
        context = {
            'liked': True
        }
        if model == 'Review':
            # 작성자에게 경험치 10 추가
            obj.user.experience += 10
            obj.user.save()
    context['count'] = obj.like_users.count()
    return JsonResponse(context)
