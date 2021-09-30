from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.ListCreateView.as_view(), name='index'),
    path('<int:pk>', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/likes', views.LikeCreateDeleteView.as_view(), name='likes'),
]
