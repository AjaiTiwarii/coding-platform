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
    RecentActivitySerializer, 
    UserProgressSerializer,
    LeaderboardSerializer,
    ProblemStatsSerializer
)

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_overview(request):
    """
    Get comprehensive dashboard overview for the authenticated user
    """
    user = request.user
    
    # User Statistics [6][7]
    total_submissions = Submission.objects.filter(user=user).count()
    accepted_submissions = Submission.objects.filter(user=user, status='ACCEPTED').count()
    
    # Problems Statistics
    problems_attempted = Submission.objects.filter(user=user).values('problem').distinct().count()
    problems_solved = Submission.objects.filter(
        user=user, 
        status='ACCEPTED'
    ).values('problem').distinct().count()
    
    # Recent Activity (last 30 days) [13]
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_submissions = Submission.objects.filter(
        user=user,
        submitted_at__gte=thirty_days_ago
    ).count()
    
    # Accuracy Rate
    accuracy_rate = (accepted_submissions / total_submissions * 100) if total_submissions > 0 else 0
    
    # Problem Difficulty Breakdown [7]
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
    
    # Language Usage Statistics [6]
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
def recent_activity(request):
    """
    Get recent activity for the authenticated user [6][18]
    """
    limit = int(request.GET.get('limit', 10))
    
    recent_submissions = Submission.objects.filter(
        user=request.user
    ).select_related('problem', 'language').order_by('-submitted_at')[:limit]
    
    serializer = RecentActivitySerializer(recent_submissions, many=True)
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
    
    # Monthly problem solving progress [18]
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leaderboard(request):
    """
    Get leaderboard data [16]
    """
    limit = int(request.GET.get('limit', 20))
    period = request.GET.get('period', 'all')  # all, monthly, weekly
    
    # Base queryset [16]
    users = User.objects.annotate(
        problems_solved=Count(
            'submission',
            filter=Q(submission__status='ACCEPTED'),
            distinct=True
        ),
        total_submissions=Count('submission'),
        avg_score=Avg('submission__score')
    ).filter(problems_solved__gt=0)
    
    # Apply time filter
    if period == 'monthly':
        start_date = timezone.now().replace(day=1)
        users = users.filter(submission__submitted_at__gte=start_date)
    elif period == 'weekly':
        start_date = timezone.now() - timedelta(days=7)
        users = users.filter(submission__submitted_at__gte=start_date)
    
    # Order by problems solved and accuracy [16]
    users = users.order_by('-problems_solved', '-avg_score')[:limit]
    
    serializer = LeaderboardSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def problem_statistics(request):
    """
    Get overall problem statistics [7]
    """
    stats = {
        'total_problems': Problem.objects.filter(is_active=True).count(),
        'problems_by_difficulty': {
            'easy': Problem.objects.filter(is_active=True, difficulty='EASY').count(),
            'medium': Problem.objects.filter(is_active=True, difficulty='MEDIUM').count(),
            'hard': Problem.objects.filter(is_active=True, difficulty='HARD').count(),
        },
        'most_popular_problems': Problem.objects.annotate(
            submission_count=Count('submission')
        ).order_by('-submission_count')[:5],
        'newest_problems': Problem.objects.filter(
            is_active=True
        ).order_by('-created_at')[:5]
    }
    
    serializer = ProblemStatsSerializer(stats)
    return Response(serializer.data)

def _get_user_streak(user):
    """Calculate user's current solving streak [18]"""
    # Get all dates when user solved problems
    solved_dates = list(
        Submission.objects.filter(
            user=user,
            status='ACCEPTED'
        ).values_list('submitted_at__date', flat=True)
        .distinct()
        .order_by('-submitted_at__date')
    )
    
    if not solved_dates:
        return {'current_streak': 0, 'longest_streak': 0}
    
    current_streak = 0
    longest_streak = 0
    temp_streak = 1
    
    # Calculate current streak
    current_date = timezone.now().date()
    if solved_dates and (current_date - solved_dates[0]).days <= 1:
        current_streak = 1
        for i in range(1, len(solved_dates)):
            if (solved_dates[i-1] - solved_dates[i]).days == 1:
                current_streak += 1
            else:
                break
    
    # Calculate longest streak
    for i in range(1, len(solved_dates)):
        if (solved_dates[i-1] - solved_dates[i]).days == 1:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 1
    
    return {
        'current_streak': current_streak,
        'longest_streak': max(longest_streak, 1) if solved_dates else 0
    }

def _get_user_achievements(user):
    """Get user achievements/badges [18]"""
    achievements = []
    
    # Problem solving achievements
    problems_solved = Submission.objects.filter(
        user=user, status='ACCEPTED'
    ).values('problem').distinct().count()
    
    if problems_solved >= 1:
        achievements.append({'name': 'First Problem', 'icon': '🎯', 'earned': True})
    if problems_solved >= 10:
        achievements.append({'name': 'Problem Solver', 'icon': '💡', 'earned': True})
    if problems_solved >= 50:
        achievements.append({'name': 'Code Warrior', 'icon': '⚔️', 'earned': True})
    if problems_solved >= 100:
        achievements.append({'name': 'Code Master', 'icon': '👑', 'earned': True})
    
    return achievements


# Additional dashboard functionality to extend your views.py [6][7]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_achievements(request):
    """Get detailed user achievements with progress tracking [18]"""
    user = request.user
    achievements = _get_detailed_achievements(user)
    return Response(achievements)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weekly_statistics(request):
    """Get weekly statistics for performance tracking [18]"""
    user = request.user
    weeks_data = []
    
    for i in range(12):
        week_start = timezone.now() - timedelta(weeks=i+1)
        week_end = week_start + timedelta(days=7)
        
        submissions = Submission.objects.filter(
            user=user,
            submitted_at__gte=week_start,
            submitted_at__lt=week_end
        )
        
        accepted = submissions.filter(status='ACCEPTED')
        problems_solved = accepted.values('problem').distinct().count()
        
        weeks_data.append({
            'week_start': week_start.strftime('%Y-%m-%d'),
            'problems_solved': problems_solved,
            'submissions_made': submissions.count(),
            'accuracy_rate': (accepted.count() / submissions.count() * 100) if submissions.count() > 0 else 0
        })
    
    return Response(list(reversed(weeks_data)))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def language_statistics(request):
    """Get detailed language usage statistics [6]"""
    user = request.user
    
    language_stats = list(
        Submission.objects.filter(user=user)
        .values('language__name', 'language__id')
        .annotate(
            total_submissions=Count('id'),
            accepted_submissions=Count('id', filter=Q(status='ACCEPTED')),
            avg_execution_time=Avg('execution_time'),
            avg_memory_used=Avg('memory_used')
        )
        .order_by('-total_submissions')
    )
    
    # Calculate accuracy for each language [11]
    for stat in language_stats:
        stat['accuracy_rate'] = (
            stat['accepted_submissions'] / stat['total_submissions'] * 100
        ) if stat['total_submissions'] > 0 else 0
    
    return Response(language_stats)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def submission_heatmap(request):
    """Get submission heatmap data for activity visualization [13]"""
    user = request.user
    year_ago = timezone.now() - timedelta(days=365)
    
    # Get daily submission counts
    daily_counts = {}
    submissions = Submission.objects.filter(
        user=user,
        submitted_at__gte=year_ago
    ).values('submitted_at__date').annotate(count=Count('id'))
    
    for submission in submissions:
        date_str = submission['submitted_at__date'].strftime('%Y-%m-%d')
        daily_counts[date_str] = submission['count']
    
    # Fill in missing dates with 0 [13]
    current_date = year_ago.date()
    end_date = timezone.now().date()
    heatmap_data = []
    
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        heatmap_data.append({
            'date': date_str,
            'count': daily_counts.get(date_str, 0)
        })
        current_date += timedelta(days=1)
    
    return Response(heatmap_data)

def _get_detailed_achievements(user):
    """Get detailed achievements with progress tracking [18]"""
    problems_solved = Submission.objects.filter(
        user=user, status='ACCEPTED'
    ).values('problem').distinct().count()
    
    total_submissions = Submission.objects.filter(user=user).count()
    
    streak_data = _get_user_streak(user)
    
    achievements = [
        {
            'name': 'First Steps',
            'description': 'Submit your first solution',
            'icon': '🚀',
            'earned': total_submissions >= 1,
            'progress': min(total_submissions, 1),
            'target': 1
        },
        {
            'name': 'Problem Solver',
            'description': 'Solve 10 problems',
            'icon': '💡',
            'earned': problems_solved >= 10,
            'progress': min(problems_solved, 10),
            'target': 10
        },
        {
            'name': 'Consistent Coder',
            'description': 'Maintain a 7-day solving streak',
            'icon': '🔥',
            'earned': streak_data['current_streak'] >= 7,
            'progress': min(streak_data['current_streak'], 7),
            'target': 7
        },
        {
            'name': 'Century Club',
            'description': 'Solve 100 problems',
            'icon': '💯',
            'earned': problems_solved >= 100,
            'progress': min(problems_solved, 100),
            'target': 100
        }
    ]
    
    return achievements
