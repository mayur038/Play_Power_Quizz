from django.contrib import admin
from django.apps import apps
from .models import Quiz,QuizHistory,Notification,Submission
# Dynamically register all models from the current app
admin.site.register(Quiz)
admin.site.register(QuizHistory)
admin.site.register(Notification)
admin.site.register(Submission)
