from django.urls import path
from . import views

urlpatterns = [
    path('activities/', views.activity_stream, name='activity'),
]