from studies.models import Study, Studying, Announcement
from django.utils import timezone
from datetime import timedelta

def alarm(request):
    if request.user.is_authenticated:
        lead_studies = Study.objects.filter(user=request.user)
        all_requests = list()
        for study in lead_studies:
            all_requests.append((study, study.join_request.all()))
        
        all_announcements = list()
        studyings = Studying.objects.filter(user=request.user)
        for studying in studyings:
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
    else:
        context = {

        }

    return context