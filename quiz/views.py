from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from .serializer import LoginSerializer,GenerateQuizSerializer,SubmitQuizSerializer,QuizHistorySerializer
from .models import Quiz, Submission,QuizHistory # Replace with actual models
from django.conf import settings

import requests
from rest_framework.decorators import api_view

QUIZ_API_KEY = "VB6YHAzJWLnTVMjQ7rtIHhKyRZlWOtIW9fC31k0p"
QUIZ_API_BASE_URL = "https://quizapi.io/api/v1/questions"

class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotifyResultsView(APIView):
    """
    API endpoint to notify quiz participants of their results via email.
    """
    permission_classes = [IsAuthenticated]  

    def post(self, request, quiz_id):
        # Fetch the quiz object
        quiz = get_object_or_404(Quiz, id=quiz_id)

        # Fetch the results of the quiz
        results = Submission.objects.filter(quiz=quiz)
        if not results.exists():
            return Response({"error": "No results found for this quiz."}, status=status.HTTP_404_NOT_FOUND)

      
        for result in results:
            email = result.user.email 
            subject = f"Your Results for Quiz: {quiz.id}"
            message = f"Hello {result.user.username},\n\nYour score is: {result.score} \n\nThanks for participating!"
            try:
                send_mail(subject, message,  settings.EMAIL_HOST_USER   , [email])
            except Exception as e:
                return Response({"error": f"Failed to send email to {email}. Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Notifications sent successfully!"}, status=status.HTTP_200_OK)

class GenerateQuizView(APIView):
    def post(self, request):
        data = request.data
        grade = data.get("grade")
        subject = data.get("subject")
        total_questions = data.get("totalQuestions", 10)
        difficulty = data.get("difficulty", "medium")

        # Call QuizAPI
        try:
            response = requests.get(
                settings.QUIZ_API_BASE_URL,
                headers={ },
                params={
                    "apiKey": settings.QUIZ_API_KEY,
                    "category": subject,
                    "difficulty": difficulty,
                    "limit": total_questions
                }
            )
            response.raise_for_status()
            quiz_data = response.json()

            # Save metadata to DB
            quiz,created = Quiz.objects.get_or_create(
                quiz_id=f"quiz_{grade}_{subject}_{difficulty}",
                grade=grade,
                subject=subject,
                total_questions=total_questions,
                max_score=total_questions,  # Assuming 1 point per question
                difficulty=difficulty,
            )
            return Response({"quizId": quiz.quiz_id, "questions": quiz_data}, status=status.HTTP_201_CREATED)

        except requests.exceptions.RequestException as e:
            return Response({"error": "Failed to generate quiz", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Submit Quiz
class SubmitQuizView(APIView):
    def post(self, request, quiz_id):
        serializer = SubmitQuizSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            try:
                # Call GrokCloud API
                groq_response = requests.post(
                    f"{GROKCLOUD_BASE_URL}quiz/evaluate",
                    headers={"Authorization": f"Bearer {GROKCLOUD_API_KEY}"},
                    json={"quizId": quiz_id, "responses": data["responses"]}
                )
                groq_response.raise_for_status()
                evaluation_data = groq_response.json()

                # Save to history
                quiz = Quiz.objects.get(quiz_id=quiz_id)
                QuizHistory.objects.create(
                    quiz=quiz,
                    score=evaluation_data['score'],
                    status=evaluation_data['status']
                )
                return Response(evaluation_data, status=status.HTTP_200_OK)

            except Quiz.DoesNotExist:
                return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)
            except requests.exceptions.RequestException:
                return Response({"error": "Failed to evaluate quiz"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Fetch Quiz History
class QuizHistoryView(APIView):
    def get(self, request):
        histories = QuizHistory.objects.select_related('quiz').all()
        serializer = QuizHistorySerializer(histories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



