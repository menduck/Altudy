from django.shortcuts import render, get_list_or_404
from studies.models import Study, Studying

def main(request):
    # 가입 중인 스터디
    # 스터디에서 접근 시 {for-each}.study.title로 접근
    studyings = Studying.objects.filter(user=request.user)
    # 최신 스터디 5개
    latest_studies = Study.objects.all().order_by('-created_at')[:5]
    
    context = {
        'studyings': studyings,
        'latest_studies': latest_studies,
    }
    return render(request, 'main.html', context)