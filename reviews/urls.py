from django.urls import path

from . import views


app_name = 'reviews'
urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/review_create/', views.review_create, name='review_create'),
    path('<int:pk>/review_update/<int:review_pk>/', views.review_update, name='review_update'),
    path('<int:pk>/review_delete/<int:review_pk>/', views.review_delete, name='review_delete'),
    path('create/', views.create, name='create'),
]
