from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.ListCreateView.as_view(), name='index'),
]