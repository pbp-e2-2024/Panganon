from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_home, name='forum_home'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('create_thread/', views.create_thread, name='create_thread'),
    path('thread/<int:thread_id>/add_post/', views.add_post, name='add_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/comment/<int:parent_id>/', views.add_comment, name='add_reply'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('post/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('threads/user/<int:user_id>/', views.threads_by_user, name='threads_by_user'),
    path('delete_thread/<int:thread_id>/', views.delete_thread, name='delete_thread'),
]