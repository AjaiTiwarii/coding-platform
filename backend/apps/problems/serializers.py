from rest_framework import serializers
from .models import Problem, Tag, TestCase

class TagSerializer(serializers.ModelSerializer):
    problem_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'description', 'color', 'problem_count', 'created_at']
    
    def get_problem_count(self, obj):
        return obj.problems.filter(is_active=True).count()

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['id', 'input_data', 'expected_output', 'is_sample', 'points', 'order']

class ProblemSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_names = serializers.StringRelatedField(source='tags', many=True, read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Problem
        fields = [
            'id', 'title', 'slug', 'difficulty', 'category', 
            'time_limit', 'memory_limit', 'tags', 'tag_names',
            'created_by_username', 'created_at', 'updated_at'
        ]

class ProblemDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    test_cases = serializers.SerializerMethodField()
    sample_test_cases = serializers.SerializerMethodField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    total_submissions = serializers.SerializerMethodField()
    success_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = Problem
        fields = [
            'id', 'title', 'slug', 'description', 'difficulty', 
            'category', 'time_limit', 'memory_limit', 'constraints',
            'sample_input', 'sample_output', 'explanation', 'hints',
            'tags', 'created_by_username', 'test_cases', 'sample_test_cases',
            'total_submissions', 'success_rate', 'created_at', 'updated_at'
        ]
    
    def get_test_cases(self, obj):
        # Only return sample test cases for regular users
        sample_cases = obj.test_cases.filter(is_sample=True).order_by('order')
        return TestCaseSerializer(sample_cases, many=True).data
    
    def get_sample_test_cases(self, obj):
        sample_cases = obj.test_cases.filter(is_sample=True).order_by('order')
        return TestCaseSerializer(sample_cases, many=True).data
    
    def get_total_submissions(self, obj):
        # This will require the submissions app to be implemented
        return getattr(obj, 'submission_count', 0)
    
    def get_success_rate(self, obj):
        # This will require the submissions app to be implemented
        return getattr(obj, 'success_rate', 0)

class ProblemCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False
    )
    
    class Meta:
        model = Problem
        fields = [
            'title', 'description', 'difficulty', 'category',
            'time_limit', 'memory_limit', 'constraints',
            'sample_input', 'sample_output', 'explanation', 'hints', 'tags'
        ]
    
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        problem = Problem.objects.create(**validated_data)
        problem.tags.set(tags)
        return problem

class TestCaseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = [
            'problem', 'input_data', 'expected_output', 
            'is_sample', 'is_hidden', 'points', 'order'
        ]
