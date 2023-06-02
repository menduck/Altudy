from django import template
from studies.models import Study

register = template.Library()

@register.filter(name="test")
def test(value, arg):
    return value + '"te+st"' + arg


@register.filter(name="alarm_exists")
def alarm_exists(value):
    studies = Study.objects.filter(user=value)
    
    for study in studies:
        if study.join_request.exists():
            return True
        
    # 기타 알람이 갈 수 있는 사항들(스터디 공지사항 등)
    # return True
    # code ...

    return False