from django.urls import path
from . import views

urlpatterns = [
    path('bag-of-words/', views.bag_of_words, name='bag_of_words'),
]