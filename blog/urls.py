from django.urls import path
from blog import views
urlpatterns = [
        # URL for the homepage or post list
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('contact/success/', views.contact_success_view, name='contact_success'),

    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    # path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('like-post/<int:post_id>/', views.like_post, name='like_post'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_post/', views.create_post, name='create_post'),
    path('update_post/<int:post_id>/', views.update_post, name='update_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/comments/', views.post_comments, name='post_comments'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),]
