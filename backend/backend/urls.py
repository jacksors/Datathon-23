# backend/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('', views.handleHome, name='home'),  # handle requests to the root URL '/'
    path('predict/', views.handlePredict, name='predict'),
    path('predict', views.handlePredict, name='predict-no-slash'),
    path('guess/', views.handleGuess, name='guess'),
    path('guess', views.handleGuess, name='guess-no-slash'),
    path('newcase/', views.handleNewCase, name='newcase'),
    path('newcase', views.handleNewCase, name='newcase-no-slash'),
    path('score/', views.handleScore, name='score'),
    path('score', views.handleScore, name='score-no-slash'),
]
