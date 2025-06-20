from rest_framework import serializers
from .models import Submission, TestCaseResult, Language

class TestCaseResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCaseResult
        fields = ('id', 'test_case', 'status', 'execution_time', 'memory_used', 'output', 'error_message')

class SubmissionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    problem_title = serializers.CharField(source='problem.title', read_only=True)
    problem_slug = serializers.CharField(source='problem.slug', read_only=True)
    language_name = serializers.CharField(source='language.name', read_only=True)
    test_results = TestCaseResultSerializer(many=True, read_only=True)
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
        read_only_fields = fields

    def get_success_rate(self, obj):
        if obj.total_test_cases > 0:
            return round((obj.test_cases_passed / obj.total_test_cases) * 100, 2)
        return 0

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name', 'version')