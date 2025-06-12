from django.db import models

# Create your model here.
from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    quiz_id = models.CharField(max_length=100)
    grade = models.IntegerField()
    subject = models.CharField(max_length=50)
    total_questions = models.IntegerField()
    max_score = models.IntegerField()
    difficulty = models.CharField(max_length=10)

 # Shows the History of Quizz
class QuizHistory(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    status = models.CharField(max_length=10)
    attempted_at = models.DateTimeField(auto_now_add=True)

class Submission(models.Model):
    """
    Stores the user's answers to a quiz, their score, and completion time.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional for mock auth
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answers = models.JSONField()  # Stores answers in a JSON format
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.user.username if self.user else 'Anonymous'} for Quiz {self.quiz.id}"


class Notification(models.Model):
    """
    Tracks email notifications sent to users after quiz submissions.
    """
    email = models.EmailField()
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE)
    suggestions = models.TextField()  # AI-generated suggestions for improvement
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.email} sent at {self.sent_at}"
