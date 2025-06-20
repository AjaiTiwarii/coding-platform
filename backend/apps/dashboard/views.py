from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Avg, Max, Min
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from apps.problems.models import Problem
from apps.submissions.models import Submission, Language
from .serializers import (
    DashboardStatsSerializer, 
    UserProgressSerializer,
)

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_overview(request):
    """
    Get comprehensive dashboard overview for the authenticated user
    """
    user = request.user
    
    # User Statistics 
    total_submissions = Submission.objects.filter(user=user).count()
    accepted_submissions = Submission.objects.filter(user=user, status='ACCEPTED').count()
    
    # Problems Statistics
    problems_attempted = Submission.objects.filter(user=user).values('problem').distinct().count()
    problems_solved = Submission.objects.filter(
        user=user, 
        status='ACCEPTED'
    ).values('problem').distinct().count()
    
    # Recent Activity 
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_submissions = Submission.objects.filter(
        user=user,
        submitted_at__gte=thirty_days_ago
    ).count()
    
    # Accuracy Rate
    accuracy_rate = (accepted_submissions / total_submissions * 100) if total_submissions > 0 else 0
    
    # Problem Difficulty Breakdown 
    difficulty_stats = {
        'easy': Submission.objects.filter(
            user=user, 
            status='ACCEPTED',
            problem__difficulty='EASY'
        ).values('problem').distinct().count(),
        'medium': Submission.objects.filter(
            user=user, 
            status='ACCEPTED',
            problem__difficulty='MEDIUM'
        ).values('problem').distinct().count(),
        'hard': Submission.objects.filter(
            user=user, 
            status='ACCEPTED',
            problem__difficulty='HARD'
        ).values('problem').distinct().count(),
    }
    
    # Language Usage Statistics
    language_stats = list(
        Submission.objects.filter(user=user)
        .values('language__name')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )
    
    dashboard_data = {
        'user_stats': {
            'total_submissions': total_submissions,
            'accepted_submissions': accepted_submissions,
            'problems_attempted': problems_attempted,
            'problems_solved': problems_solved,
            'accuracy_rate': round(accuracy_rate, 2),
            'recent_submissions': recent_submissions
        },
        'difficulty_breakdown': difficulty_stats,
        'language_usage': language_stats,
        'streak_data': _get_user_streak(user),
        'achievements': _get_user_achievements(user)
    }
    
    serializer = DashboardStatsSerializer(dashboard_data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_progress(request):
    """
    Get user progress data for charts and visualizations [7][13]
    """
    user = request.user
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    # Daily submission count
    daily_submissions = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        next_date = date + timedelta(days=1)
        
        count = Submission.objects.filter(
            user=user,
            submitted_at__gte=date,
            submitted_at__lt=next_date
        ).count()
        
        daily_submissions.append({
            'date': date.strftime('%Y-%m-%d'),
            'submissions': count
        })
    
    # Monthly problem solving progress
    monthly_solved = []
    for i in range(6):  # Last 6 months
        date = timezone.now() - timedelta(days=30*i)
        start_month = date.replace(day=1)
        if i == 0:
            end_month = timezone.now()
        else:
            end_month = (start_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        solved_count = Submission.objects.filter(
            user=user,
            status='ACCEPTED',
            submitted_at__gte=start_month,
            submitted_at__lte=end_month
        ).values('problem').distinct().count()
        
        monthly_solved.append({
            'month': start_month.strftime('%Y-%m'),
            'problems_solved': solved_count
        })
    
    progress_data = {
        'daily_submissions': daily_submissions,
        'monthly_progress': list(reversed(monthly_solved))
    }
    
    serializer = UserProgressSerializer(progress_data)
    return Response(serializer.data)

