from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.problems.models import Problem
from apps.submissions.models import Submission

User = get_user_model()

class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for comprehensive dashboard statistics [9][10]"""
    user_stats = serializers.DictField()
    difficulty_breakdown = serializers.DictField()
    language_usage = serializers.ListField()
    streak_data = serializers.DictField()
    achievements = serializers.ListField()

class RecentActivitySerializer(serializers.ModelSerializer):
    """Serializer for user's recent submission activity [9][15]"""
    problem_title = serializers.CharField(source='problem.title', read_only=True)
    problem_slug = serializers.CharField(source='problem.slug', read_only=True)
    problem_difficulty = serializers.CharField(source='problem.difficulty', read_only=True)
    language_name = serializers.CharField(source='language.name', read_only=True)
    time_ago = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Submission
        fields = [
            'id', 'problem_title', 'problem_slug', 'problem_difficulty',
            'language_name', 'status', 'status_display', 'score',
            'execution_time', 'memory_used', 'submitted_at', 'time_ago'
        ]
    
    def get_time_ago(self, obj):
        """Calculate time since submission [11]"""
        from django.utils.timesince import timesince
        return timesince(obj.submitted_at)

class UserProgressSerializer(serializers.Serializer):
    """Serializer for user progress data visualization [15]"""
    daily_submissions = serializers.ListField()
    monthly_progress = serializers.ListField()

class LeaderboardUserSerializer(serializers.ModelSerializer):
    """Serializer for individual user in leaderboard [16]"""
    problems_solved = serializers.IntegerField(read_only=True)
    total_submissions = serializers.IntegerField(read_only=True)
    accuracy_rate = serializers.SerializerMethodField()
    avg_score = serializers.FloatField(read_only=True)
    rank = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'problems_solved', 'total_submissions', 'accuracy_rate',
            'avg_score', 'rank', 'date_joined'
        ]
    
    def get_accuracy_rate(self, obj):
        """Calculate user's accuracy rate [11]"""
        if obj.total_submissions > 0:
            accepted = Submission.objects.filter(
                user=obj, status='ACCEPTED'
            ).count()
            return round((accepted / obj.total_submissions) * 100, 2)
        return 0
    
    def get_rank(self, obj):
        """Get user's rank in leaderboard [16]"""
        return getattr(obj, '_rank', None)

class LeaderboardSerializer(serializers.Serializer):
    """Serializer for leaderboard data with ranking [16]"""
    def to_representation(self, queryset):
        # Add rank to each user
        ranked_users = []
        for index, user in enumerate(queryset, 1):
            user._rank = index
            ranked_users.append(user)
        
        return LeaderboardUserSerializer(ranked_users, many=True).data

class SimpleProblemSerializer(serializers.ModelSerializer):
    """Simplified problem serializer for statistics [15]"""
    submission_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Problem
        fields = ['id', 'title', 'slug', 'difficulty', 'submission_count', 'created_at']

class ProblemStatsSerializer(serializers.Serializer):
    """Serializer for problem statistics overview [15]"""
    total_problems = serializers.IntegerField()
    problems_by_difficulty = serializers.DictField()
    most_popular_problems = SimpleProblemSerializer(many=True)
    newest_problems = SimpleProblemSerializer(many=True)

class UserStatsSerializer(serializers.Serializer):
    """Serializer for detailed user statistics [11]"""
    total_submissions = serializers.IntegerField()
    accepted_submissions = serializers.IntegerField()
    problems_solved = serializers.IntegerField()
    accuracy_rate = serializers.FloatField()
    current_streak = serializers.IntegerField()
    longest_streak = serializers.IntegerField()
    favorite_language = serializers.CharField()
    
class WeeklyProgressSerializer(serializers.Serializer):
    """Serializer for weekly progress tracking [18]"""
    week_start = serializers.DateField()
    problems_solved = serializers.IntegerField()
    submissions_made = serializers.IntegerField()
    accuracy_rate = serializers.FloatField()

class AchievementSerializer(serializers.Serializer):
    """Serializer for user achievements and badges [18]"""
    name = serializers.CharField()
    description = serializers.CharField()
    icon = serializers.CharField()
    earned = serializers.BooleanField()
    earned_date = serializers.DateTimeField(required=False)
    progress = serializers.IntegerField(required=False)
    target = serializers.IntegerField(required=False)
