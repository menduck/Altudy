from studies.models import Study, Studying, Announcement
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required

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
        announcements = Announcement.objects.filter(
            study=studying.study, 
            updated_at__gte=timezone.now() - timedelta(days=7)
            )
        all_announcements.append(announcements)
    context = {
        'all_requests': all_requests,
        'all_announcements': all_announcements,
    }

    return context