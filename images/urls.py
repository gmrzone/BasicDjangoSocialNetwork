from django.urls import path
from . import views




urlpatterns = [
    path('create-image-post/', views.image_post, name='create_image'),
    path('<slug:slug>/<int:year>/<int:month>/<int:day>/', views.post_detail, name='post_detail'),
    path('like_image/', views.like_image, name='like_image'),
]