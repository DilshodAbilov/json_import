from django.urls import path

from .views import top_languages_year
urlpatterns = [
    path('top/languages/',top_languages_year,name = 'top_languages'),
]