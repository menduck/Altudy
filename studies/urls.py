from django.urls import path
from . import views


app_name = 'studies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:study_pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:study_pk>/delete/', views.delete, name='delete'),
    path('<int:study_pk>/update/', views.update, name='update'),
    path('<int:study_pk>/join/', views.join, name='join'), # 스터디 가입, 가입 요청
    path('<int:study_pk>/withdraw/', views.withdraw, name='withdraw'), # 스터디 탈퇴
    path('<int:study_pk>/accept/<username>/', views.accept, name='accept'), # 스터디 가입 요청 수락
    path('<int:study_pk>/reject/<username>/', views.reject, name='reject'), # 스터디 가입 요청 거절
    path('<int:study_pk>/expel/<username>/', views.expel, name='expel'), # 스터디원 방출
    path('<int:study_pk>/cancel/', views.cancel, name='cancel'), # 스터디 가입 요청 취소
    
    # 알람 페이지 -임시-
    path('alarm/', views.alarm, name='alarm'),

    # mainboard
    path('<int:study_pk>/mainboard/', views.mainboard, name='mainboard'),
]