from django.urls import path
from . import views


urlpatterns = [  
    path('<int:id>/', views.detail_news, name='detail_news'),
    path('', views.main, name='main'),
]