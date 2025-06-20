from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Submission, Language
from .serializers import SubmissionSerializer, LanguageSerializer
from apps.problems.models import Problem
from .services import CodeExecutionService

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_code(request):
    user = request.user
    code = request.data.get('code')
    language_id = request.data.get('language')
    problem_id = request.data.get('problem')

    if not all([code, language_id, problem_id]):
        return Response({"error": "Missing required fields."}, status=400)

    try:
        problem = Problem.objects.get(id=problem_id)
        language = Language.objects.get(id=language_id)
    except:
        return Response({"error": "Invalid problem or language."}, status=400)

    submission = Submission.objects.create(
        user=user,
        problem=problem,
        language=language,
        code=code,
        status='PENDING'
    )

    CodeExecutionService.execute_submission(submission.id)
    serializer = SubmissionSerializer(submission)
    return Response(serializer.data, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_submissions(request):
    submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')
    serializer = SubmissionSerializer(submissions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def submission_detail(request, pk):
    try:
        submission = Submission.objects.get(pk=pk, user=request.user)
    except Submission.DoesNotExist:
        return Response({"error": "Submission not found."}, status=404)
    serializer = SubmissionSerializer(submission)
    return Response(serializer.data)

class LanguageListView(generics.ListAPIView):
    queryset = Language.objects.filter(is_active=True)
    serializer_class = LanguageSerializer