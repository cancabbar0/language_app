from . import views
from django.urls import path

urlpatterns = [
    path('', views.home_view, name='home'),
    path('add_word/', views.add_word_view, name='add_word'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('settings/', views.settings_view, name='settings'),
    path('analyze_report/', views.get_analize_report, name='get_analize_report'),
]
