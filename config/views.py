from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone
import pytz

from studies.models import Study, Studying, Announcement, AnnouncementRead
from django.db.models import Count
from studies.models import LANGUAGE_CHOICES

def main(request):
    # 가입 중인 스터디
    # 스터디에서 접근 시 {for-each}.study.title로 접근
    if request.user.is_authenticated:
        studyings = Studying.objects.filter(user=request.user)
        for studying in studyings:
            # studying.announcements_count = Announcement.objects.filter(
            #     study=studying.study,
            #     updated_at__gte=timezone.now() - timedelta(days=7)
            #     ).count()
            studying.announcements_count = AnnouncementRead.objects.filter(
                announcement__in=Announcement.objects.filter(study=studying.study, updated_at__gte=timezone.now() - timedelta(days=7)),
                user=request.user,
                is_read=False
            ).count()
    else:
        studyings = None
    # 최신 스터디 16개
    latest_studies = Study.objects.annotate(
        member_num=Count('studying_users')
        ).order_by('-created_at')[:16]
    
    
    context = {
        'studyings': studyings,
        'latest_studies': latest_studies,
        'LANGUAGE_CHOICES': LANGUAGE_CHOICES,
    }
    return render(request, 'main.html', context)


@login_required
def alarm(request):
    lead_studies = Study.objects.filter(user=request.user)
    all_requests = list()
    for study in lead_studies:
        all_requests.append((study, study.join_request.all()))
    
    all_announcements = list()
    studyings = Studying.objects.filter(user=request.user)
    for studying in studyings:
        # 최근 일주일 간의 공지만 표시
        # announcements = Announcement.objects.filter(
        #     study=studying.study, 
        #     updated_at__gte=timezone.now() - timedelta(days=7),
        #     )
        announcements = Announcement.objects.filter(
            study=studying.study, 
            updated_at__gte=timezone.now() - timedelta(days=7),
            announcementread__is_read=False,
            announcementread__user=request.user,
            )
        all_announcements.append(announcements)
    
    context = {
        'all_requests': all_requests,
        'all_announcements': all_announcements,
    }
    return render(request, 'alarm.html', context)