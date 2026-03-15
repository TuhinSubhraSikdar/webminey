from django.urls import path
from .views import bag_of_words_view

urlpatterns = [
    path('bag-of-words/', bag_of_words_view, name='bag_of_words'),
]