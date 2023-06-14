from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import ChatRooms
from studies.models import Study
from reviews.models import Problem, Review

# Create your views here.
@login_required
def room(request, study_pk: int):
    me = request.user
    study = get_object_or_404(Study, pk=study_pk)
    if not study.studying_users.filter(pk=me.pk).exists():
        return redirect('studies:detail', study_pk)

    room = ChatRooms.objects.get_or_create(title=str(study_pk))
    problems = study.problem_set.all()

    context = {
        'room_name': study_pk,
        'problems': problems,
    }
    return render(request, "chat/room.html", context)


def get_review_content(request, review_pk: int):
    review = get_object_or_404(Review, pk=review_pk)
    context = {
        'content': review.content,
    }
    return JsonResponse(context)


@login_required
def room_delete(request, study_pk):
    me = request.user
    study = get_object_or_404(Study, pk=study_pk)
    if not study.studying_users.filter(pk=me.pk).exists():
        return redirect('studies:detail', study_pk)
    
    # 조건 충족 시 미팅 룸 삭제
    # 조건은 js로?
    # ...

    return redirect('studies:mainboard', study_pk)


@login_required
def problems(request, study_pk: int):
    me = request.user
    study = get_object_or_404(Study, pk=study_pk)
    if not study.studying_users.filter(pk=me.pk).exists():
        return redirect('studies:detail', study_pk)
    
    problems = study.problem_set.all()

    context = {
        'problems': problems,
        'study_pk': study_pk,
    }
    return render(request, 'chat/problems.html', context)


@login_required
def reviews(request, study_pk: int, problem_pk: int):
    me = request.user
    study = get_object_or_404(Study, pk=study_pk)
    if not study.studying_users.filter(pk=me.pk).exists():
        return redirect('studies:detail', study_pk)
    
    reviews = get_object_or_404(Problem, pk=problem_pk).review_set.all()
    
    context = {
        'reviews': reviews,
        'study_pk': study_pk,
        'problem_pk': problem_pk,
    }
    return render(request, 'chat/reviews.html', context)


@login_required
def review_detail(request, study_pk: int, problem_pk: int, review_pk: int):
    me = request.user
    study = get_object_or_404(Study, pk=study_pk)
    if not study.studying_users.filter(pk=me.pk).exists():
        return redirect('studies:detail', study_pk)
    
    problem = get_object_or_404(Problem, pk=problem_pk)
    review = get_object_or_404(Review, pk=review_pk)
    
    context = {
        'problem': problem,
        'review': review,
        'study_pk': study_pk,
        'problem_pk': problem_pk,
    }
    return render(request, 'chat/review_detail.html', context)