# backend/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('', views.handleHome, name='home'),  # handle requests to the root URL '/'
    path('predict/', views.handlePredict, name='predict'),
    path('guess/', views.handleGuess, name='guess'),
    path('newcase/', views.handleNewCase, name='newcase'),
    path('score/', views.handleScore, name='score'),
]
