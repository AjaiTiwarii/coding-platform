from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Submission, Language, TestCaseResult
from apps.problems.models import Problem
from apps.problems.serializers import ProblemSerializer
from .models import Submission

User = get_user_model()

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = [
            'id', 'name', 'version', 'file_extension', 
            'is_active', 'time_multiplier', 'memory_multiplier'
        ]

class TestCaseResultSerializer(serializers.ModelSerializer):
    test_case_input = serializers.CharField(source='test_case.input_data', read_only=True)
    test_case_expected = serializers.CharField(source='test_case.expected_output', read_only=True)
    test_case_points = serializers.IntegerField(source='test_case.points', read_only=True)
    is_sample = serializers.BooleanField(source='test_case.is_sample', read_only=True)
    
    class Meta:
        model = TestCaseResult
        fields = [
            'id', 'status', 'execution_time', 'memory_used', 
            'output', 'error_message', 'test_case_input', 
            'test_case_expected', 'test_case_points', 'is_sample', 'created_at'
        ]




class SubmissionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    problem_title = serializers.CharField(source='problem.title', read_only=True)
    problem_slug = serializers.CharField(source='problem.slug', read_only=True)
    language_name = serializers.CharField(source='language.name', read_only=True)
    test_results = TestCaseResultSerializer(many=True, read_only=True)
    submitted_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    success_rate = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = [
            'id', 'username', 'problem_title', 'problem_slug',
            'language_name', 'code', 'status', 'score',
            'execution_time', 'memory_used', 'test_cases_passed',
            'total_test_cases', 'error_message', 'submitted_at',
            'judged_at', 'is_best_submission', 'test_results', 'success_rate'
        ]
        read_only_fields = [
            'status', 'score', 'execution_time', 'memory_used',
            'test_cases_passed', 'total_test_cases', 'error_message',
            'submitted_at', 'judged_at', 'is_best_submission'
        ]

    def get_success_rate(self, obj):
        if obj.total_test_cases > 0:
            return round((obj.test_cases_passed / obj.total_test_cases) * 100, 2)
        return 0


class SubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['problem', 'language', 'code']
        
    def validate_problem(self, value):
        if not value.is_active:
            raise serializers.ValidationError("This problem is not active.")
        return value
    
    def validate_language(self, value):
        if not value.is_active:
            raise serializers.ValidationError("This language is not supported.")
        return value
    
    def validate_code(self, value):
        if not value.strip():
            raise serializers.ValidationError("Code cannot be empty.")
        if len(value) > 50000:  # 50KB limit
            raise serializers.ValidationError("Code is too long. Maximum 50KB allowed.")
        return value

class SubmissionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing submissions"""
    username = serializers.CharField(source='user.username', read_only=True)
    problem_title = serializers.CharField(source='problem.title', read_only=True)
    problem_slug = serializers.CharField(source='problem.slug', read_only=True)
    language_name = serializers.CharField(source='language.name', read_only=True)
    success_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = Submission
        fields = [
            'id', 'username', 'problem_title', 'problem_slug',
            'language_name', 'status', 'score', 'execution_time',
            'memory_used', 'test_cases_passed', 'total_test_cases',
            'submitted_at', 'is_best_submission', 'success_rate'
        ]
    
    def get_success_rate(self, obj):
        if obj.total_test_cases > 0:
            return round((obj.test_cases_passed / obj.total_test_cases) * 100, 2)
        return 0

class SubmissionStatsSerializer(serializers.Serializer):
    """Serializer for submission statistics"""
    total_submissions = serializers.IntegerField()
    accepted_submissions = serializers.IntegerField()
    success_rate = serializers.FloatField()
    favorite_language = serializers.CharField()
    avg_execution_time = serializers.FloatField()
    problems_solved = serializers.IntegerField()
    
class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for leaderboard data"""
    username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    problem_title = serializers.CharField(source='problem.title', read_only=True)
    language_name = serializers.CharField(source='language.name', read_only=True)
    
    class Meta:
        model = Submission
        fields = [
            'id', 'username', 'user_email', 'problem_title',
            'language_name', 'score', 'execution_time', 'memory_used',
            'submitted_at'
        ]
