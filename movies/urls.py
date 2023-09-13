from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.movie_detail, name='movie_detail'),
    path('participant/<int:id>/', views.participant_detail, name='participant_detail'),
    path('<int:id>/comments/create/', views.comments_create, name='comments_create'),

    path('comments/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
]