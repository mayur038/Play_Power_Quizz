from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Quiz, QuizHistory

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")

        user = authenticate(username=username, password=password)

        if user is None:
            # Create a user for mock purposes
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
            data["user"] = user
        else:
            data["user"] = user

        return data

class GenerateQuizSerializer(serializers.Serializer):
    grade = serializers.IntegerField(min_value=1, max_value=12)
    subject = serializers.CharField(max_length=50)
    totalQuestions = serializers.IntegerField(min_value=1, max_value=50)
    maxScore = serializers.IntegerField(min_value=1, max_value=100)
    difficulty = serializers.ChoiceField(choices=["EASY", "MEDIUM", "HARD"])

class SubmitQuizSerializer(serializers.Serializer):
    quizId = serializers.CharField(max_length=100)
    responses = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )

class QuizHistorySerializer(serializers.ModelSerializer):
    quizId = serializers.CharField(source='quiz.quiz_id')

    class Meta:
        model = QuizHistory
        fields = ['quizId', 'score', 'status', 'attempted_at']
