from django.urls import path
from . import views_api

urlpatterns = [
    path('posts/', views_api.post_list_create),
    path('posts/<int:pk>/', views_api.post_detail),
]