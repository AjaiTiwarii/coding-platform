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


class UserProgressSerializer(serializers.Serializer):
    """Serializer for user progress data visualization [15]"""
    daily_submissions = serializers.ListField()
    monthly_progress = serializers.ListField()

