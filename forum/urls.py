from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_home, name='forum_home'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('create_thread/', views.create_thread, name='create_thread'),
    path('create_thread_flutter/', views.create_thread_flutter, name='create_thread_flutter'),
    path('thread/<int:thread_id>/add_post/', views.add_post, name='add_post'),
    path('thread/<int:thread_id>/add_post_flutter/', views.add_post_flutter, name='add_post_flutter'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/comment_flutter/', views.add_comment_flutter, name='add_comment_flutter'),
    path('post/<int:post_id>/comment/<int:parent_id>/', views.add_comment, name='add_reply'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('post/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('post_edit_flutter/', views.edit_post_flutter, name='edit_post_flutter'),
    path('comment_edit_flutter/', views.edit_comment_flutter, name='edit_comment_flutter'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('threads/user/<int:user_id>/', views.threads_by_user, name='threads_by_user'),
    path('delete_thread/<int:thread_id>/', views.delete_thread, name='delete_thread'),
    path('delete_thread_flutter/', views.delete_thread_flutter, name='delete_thread_flutter'),
    path('delete_post_flutter/', views.delete_post_flutter, name='delete_post_flutter'),
    path('delete_comment_flutter/', views.delete_comment_flutter, name='delete_comment_flutter'),
    path('view/', views.view_id, name='view_id'),
]