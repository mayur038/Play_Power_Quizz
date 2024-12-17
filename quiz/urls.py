from django.urls import path
from .views import LoginView, NotifyResultsView,NotifyResultsView,SubmitQuizView,GenerateQuizView,QuizHistoryView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('<int:quiz_id>/notify/', NotifyResultsView.as_view(), name='notify_results'),
    path('quiz/', GenerateQuizView.as_view(), name='generate_quiz'),
    path('quiz/<str:quiz_id>/submit/', SubmitQuizView.as_view(), name='submit_quiz'),
    path('quiz/history/', QuizHistoryView.as_view(), name='quiz_history'),
]