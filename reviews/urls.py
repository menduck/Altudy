from django.urls import path

from . import views


app_name = 'detail'
urlpatterns = [
    path('<int:pk>/', views.detail, name='detail')
]
