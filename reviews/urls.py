from django.urls import path

from . import views


app_name = 'reviews'
urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
]
