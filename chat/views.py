from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import ChatRooms
from studies.models import Study

# Create your views here.
@login_required
def room(request, study_pk: int):
    me = request.user
    study = get_object_or_404(Study, pk=study_pk)
    if not study.studying_users.filter(pk=me.pk).exists():
        return redirect('studies:detail', study_pk)

    room = ChatRooms.objects.get_or_create(title=str(study_pk))

    return render(request, "chat/room.html", {"room_name": study_pk})


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