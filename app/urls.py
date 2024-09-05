from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about_view, name="about"),
    path('budget-view/', views.budget_view),
    path('take-quiz/', views.take_quiz_, name='take_quiz_'),
    path('quiz/', views.quiz_view, name='quiz_view'),
    path('quiz/result/<int:question_id>/', views.quiz_result_view, name='quiz_result_view'),
    path('search/', views.search_view, name='search_view'),
    path('search/results/', views.search_results_view, name='search_results_view'),
]
