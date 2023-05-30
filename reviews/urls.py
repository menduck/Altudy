from django.urls import path

from . import views


app_name = 'reviews'
urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/review_create/', views.review_create, name='review_create'),
    path('create/', views.create, name='create'),
]
