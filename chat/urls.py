from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    path("<int:study_pk>/", views.room, name="room"),
    path("review/<int:review_pk>/", views.get_review_content, name="review"),
    
    path("<int:study_pk>/delete/", views.room_delete, name="room_delete"),
    
    # for fetch
    path("<int:study_pk>/problems/", views.problems, name="problems"),
    path("<int:study_pk>/problems/<int:problem_pk>/reviews/", views.reviews, name="reviews"),
    path("<int:study_pk>/problems/<int:problem_pk>/reviews/<int:review_pk>/", views.review_detail, name="review_detail"),
    ]