from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, Avg, Max
from django.utils import timezone
from datetime import timedelta
import requests


from .models import Submission, Language, TestCaseResult
from .serializers import (
    SubmissionSerializer, 
    SubmissionCreateSerializer, 
    SubmissionListSerializer,
    LanguageSerializer,
    TestCaseResultSerializer,
    LeaderboardSerializer
)
from .services import CodeExecutionService

# additional
from rest_framework.pagination import PageNumberPagination

class LanguageListView(generics.ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # 🔁 disables pagination

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Submission, Language
from .serializers import SubmissionSerializer
from apps.problems.models import Problem
import requests


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_code(request):
    user = request.user
    code = request.data.get('code')
    language_id = request.data.get('language')
    problem_id = request.data.get('problem')

    print(f"📥 User: {user.email}")
    print(f"📥 Received code: {code[:40]}")
    print(f"📥 Language ID: {language_id}, Problem ID: {problem_id}")

    if not all([code, language_id, problem_id]):
        return Response({"error": "Missing required fields."}, status=400)

    try:
        problem = Problem.objects.get(id=problem_id)
        language = Language.objects.get(id=language_id)
    except Problem.DoesNotExist:
        return Response({"error": "Invalid problem."}, status=400)
    except Language.DoesNotExist:
        return Response({"error": "Invalid language."}, status=400)

    # Create submission (status initially is 'PENDING')
    submission = Submission.objects.create(
        user=user,
        problem=problem,
        language=language,
        code=code,
    )

    # Trigger async execution via Celery
    from .services import CodeExecutionService
    CodeExecutionService.execute_submission(submission.id)

    # Return initial response
    from .serializers import SubmissionSerializer
    serializer = SubmissionSerializer(submission)
    return Response(serializer.data, status=201)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_submissions(request):
    submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')
    serializer = SubmissionSerializer(submissions, many=True)
    return Response(serializer.data)



class SubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing code submissions with CRUD operations
    """
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user).order_by('-submitted_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SubmissionCreateSerializer
        return SubmissionSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        submission = serializer.save(user=request.user)
        
        # Execute code asynchronously
        CodeExecutionService.execute_submission(submission.id)
        
        return Response(
            SubmissionSerializer(submission).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'])
    def languages(self, request):
        """Get list of available programming languages"""
        languages = Language.objects.filter(is_active=True)
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)

class LanguageListView(generics.ListAPIView):
    """
    API view to list all active programming languages
    """
    queryset = Language.objects.filter(is_active=True)
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated]

class LanguageDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve details of a specific programming language
    """
    queryset = Language.objects.filter(is_active=True)
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated]

class SubmissionResultView(APIView):
    """
    API view to get detailed results of a submission including test case results
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, submission_id):
        submission = get_object_or_404(
            Submission, 
            id=submission_id, 
            user=request.user
        )
        test_results = submission.test_results.all().order_by('test_case__order')
        
        return Response({
            'submission': SubmissionSerializer(submission).data,
            'test_results': TestCaseResultSerializer(test_results, many=True).data
        })

class RejudgeSubmissionView(APIView):
    """
    API view to rejudge a submission by resetting its status and re-executing
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, submission_id):
        submission = get_object_or_404(
            Submission, 
            id=submission_id, 
            user=request.user
        )
        
        # Reset submission status and clear previous results
        submission.status = 'PENDING'
        submission.test_results.all().delete()
        submission.save()
        
        # Re-execute the submission
        CodeExecutionService.execute_submission(submission.id)
        
        return Response({
            'message': 'Submission queued for rejudging',
            'submission_id': submission.id
        })

class MySubmissionListView(generics.ListAPIView):
    """
    API view to list current user's submissions
    """
    serializer_class = SubmissionListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Submission.objects.filter(
            user=self.request.user
        ).select_related('problem', 'language').order_by('-submitted_at')

class UserSubmissionListView(generics.ListAPIView):
    """
    API view to list submissions by a specific user
    """
    serializer_class = SubmissionListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Submission.objects.filter(
            user_id=user_id
        ).select_related('problem', 'language').order_by('-submitted_at')

class ProblemSubmissionListView(generics.ListAPIView):
    """
    API view to list all submissions for a specific problem
    """
    serializer_class = SubmissionListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        problem_id = self.kwargs['problem_id']
        return Submission.objects.filter(
            problem_id=problem_id
        ).select_related('problem', 'language', 'user').order_by('-submitted_at')

class SubmissionStatsView(APIView):
    """
    API view to get submission statistics for the current user
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_submissions = Submission.objects.filter(user=request.user)
        
        stats = {
            'total_submissions': user_submissions.count(),
            'accepted_submissions': user_submissions.filter(status='ACCEPTED').count(),
            'problems_solved': user_submissions.filter(status='ACCEPTED').values('problem').distinct().count(),
            'favorite_language': user_submissions.values('language__name').annotate(
                count=Count('id')
            ).order_by('-count').first(),
            'avg_execution_time': user_submissions.aggregate(
                avg_time=Avg('execution_time')
            )['avg_time'] or 0,
        }
        
        if stats['total_submissions'] > 0:
            stats['success_rate'] = (stats['accepted_submissions'] / stats['total_submissions']) * 100
        else:
            stats['success_rate'] = 0
            
        return Response(stats)

class LeaderboardView(generics.ListAPIView):
    """
    API view to display leaderboard of best submissions
    """
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Submission.objects.filter(
            status='ACCEPTED',
            is_best_submission=True
        ).select_related('user', 'problem', 'language').order_by('execution_time')[:100]

class SubmissionStatusView(APIView):
    """
    API view to get real-time status of a submission
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, submission_id):
        submission = get_object_or_404(
            Submission, 
            id=submission_id, 
            user=request.user
        )
        
        return Response({
            'id': submission.id,
            'status': submission.status,
            'progress': self.get_execution_progress(submission),
            'message': self.get_status_message(submission)
        })
    
    def get_execution_progress(self, submission):
        """Calculate execution progress percentage"""
        if submission.status in ['PENDING']:
            return 0
        elif submission.status == 'RUNNING':
            return 50
        else:
            return 100
    
    def get_status_message(self, submission):
        """Get user-friendly status message"""
        messages = {
            'PENDING': 'Submission is in queue...',
            'RUNNING': 'Executing your code...',
            'ACCEPTED': 'All test cases passed!',
            'WRONG_ANSWER': f'Failed {submission.total_test_cases - submission.test_cases_passed} test cases',
            'TIME_LIMIT_EXCEEDED': 'Your solution is too slow',
            'MEMORY_LIMIT_EXCEEDED': 'Your solution uses too much memory',
            'COMPILATION_ERROR': 'Code compilation failed',
            'RUNTIME_ERROR': 'Runtime error occurred',
        }
        return messages.get(submission.status, 'Unknown status')
