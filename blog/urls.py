from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path('post/<int:id>/', views.Post_detail,name='post_detail'),
    path('register/',views.register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('like/<int:post_id>/',views.like_post,name='like_post'),
    path('delete-post/<int:post_id>/',views.delete_post,name='delete_post'),
    path('create-post/',views.create_post,name='create_post'),
    path('edit/<int:post_id>/',views.edit_post,name='edit_post'),
]   
