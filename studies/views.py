from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from taggit.models import Tag
from django.db.models import Count

from .models import Study, Studying, Announcement
from .forms import StudyForm

# Create your views here.
def index(request):
    studies = Study.objects.all()
    
    context = {
        'studies': studies,
    }
    return render(request, 'studies/index.html', context)


def detail(request, study_pk: int):
    study = get_object_or_404(Study, pk=study_pk)
    # days = [day.label for day in study.days]
    
    # 현재 스터디 가입 여부 is_studying
    if study.study_studyings.filter(user=request.user).exists():
        # 스터디 가입
        is_studying = True
    else:
        # 스터디 미가입
        is_studying = False
        
    context = {
        'study': study,
        'is_studying': is_studying,
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
            
            # Tag 저장
            form.save_m2m()
            
            # 스터디장 권한(permission) 3으로 Studying 테이블에 추가
            # 임시 스터디장 혹은 부스터디장 권한(permission) 2 예정
            Studying.objects.create(study=study, user=request.user, permission=3)
            
            return redirect('studies:detail', study.pk)
    else:
        form = StudyForm()
        
    context = {
        'form': form,
    }
    return render(request, 'studies/create.html', context)


def update(request, study_pk: int):
    study = get_object_or_404(Study, pk=study_pk)
    
    # 스터디장만 수정 가능
    if request.user != study.user:
        return redirect('studies:detail', study_pk)
    
    if request.method == 'POST':
        form = StudyForm(data=request.POST, instance=study)
        if form.is_valid():
            # taggit을 위해 commit=False 후 save_m2m()
            study = form.save(commit=False)
            study.save()
            form.save_m2m()
            
            return redirect('studies:detail', study_pk)
    else:
        form = StudyForm(instance=study)
        
    context = {
        'study_pk': study_pk,
        'form': form,
    }
    return render(request, 'studies/update.html', context)


def delete(request, study_pk: int):
    study = get_object_or_404(Study, pk=study_pk)
    
    # 스터디장만 삭제 가능
    if request.user == study.user:
        try:
            study.delete()
            return redirect('/')
        finally:
            Tag.objects.annotate(ntag=Count('taggit_taggeditem_items')).filter(ntag=0).delete()
        
    
    return redirect('studies:index')


@login_required
def join(request, study_pk: int):
    study = get_object_or_404(Study, pk=study_pk)
    me = request.user
    
    studying = Studying.objects.get_or_create(study=study, user=me)
    
    return redirect('studies:detail', study_pk)
    

@login_required
def withdraw(request, study_pk: int):
    study = get_object_or_404(Study, pk=study_pk)
    me = request.user
    
    studying = Studying.objects.filter(study=study, user=me)
    if studying.exists():
        studying.first().delete()
        # 스터디장이 탈퇴할때
        if me == study.user:
            # 남은 스터디원이 있을 경우 다음 스터디장(가입 빠른순) 지정
            if Study.objects.filter(study=study).exists():
                next_studying = Studying.objects.filter(study=study).first()
                next_studying.permission = 3
                new_leader = next_studying.user
                study.user = new_leader
            else:
                # 스터디에 남은 인원이 0명일 경우?
                # code ... 
                pass
        
    return redirect('studies:detail', study_pk)


# 스터디 가입 요청 시 수락
def accept(request, study_pk: int, username: int):
    study = get_object_or_404(Study, pk=study_pk)
    person = get_user_model().objects.get(username=username)
    me = request.user
    
    # 스터디장 혹은 부스터디장(permission > 1)인 유저만 스터디 가입 허가
    # if Studying.objects.filter(study=study, user=me, permission__gte=2).exists():
    #     studying = Studying.objects.get_or_create(study=study, user=person)
    
    return redirect('studies:detail', study_pk)


# 스터디에서 해당 유저 방출
def expel(request, study_pk: int, username: int):
    study = get_object_or_404(Study, pk=study_pk)
    person = get_user_model().objects.get(username=username)
    me = request.user
    
    # 스터디장인 유저만 방출 스터디원 방출 가능
    # if Studying.objects.filter(study=study, user=me, permission__gte=2).exists():
    #     studying = Studying.objects.filter(study=study, user=person)
    #     studying.first().delete()
    
    return redirect('studies:detail', study_pk)
