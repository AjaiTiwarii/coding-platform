from django.db import models
from django.contrib.auth import get_user_model
from apps.problems.models import Problem, TestCase

User = get_user_model()

class Language(models.Model):
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=20)
    file_extension = models.CharField(max_length=10)
    compile_command = models.TextField(blank=True)
    execute_command = models.TextField()
    is_active = models.BooleanField(default=True)
    time_multiplier = models.FloatField(default=1.0)
    memory_multiplier = models.FloatField(default=1.0)

    judge0_id = models.IntegerField(null=True, blank=True)

class Submission(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('ACCEPTED', 'Accepted'),
        ('WRONG_ANSWER', 'Wrong Answer'),
        ('TIME_LIMIT_EXCEEDED', 'Time Limit Exceeded'),
        ('MEMORY_LIMIT_EXCEEDED', 'Memory Limit Exceeded'),
        ('COMPILATION_ERROR', 'Compilation Error'),
        ('RUNTIME_ERROR', 'Runtime Error'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    code = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING')
    score = models.IntegerField(default=0)
    execution_time = models.IntegerField(default=0)  # milliseconds
    memory_used = models.FloatField(default=0)  # MB
    test_cases_passed = models.IntegerField(default=0)
    total_test_cases = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    judged_at = models.DateTimeField(null=True, blank=True)
    is_best_submission = models.BooleanField(default=False)
    output = models.TextField(blank=True, null=True)

class TestCaseResult(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='test_results')
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    status = models.CharField(max_length=30)
    execution_time = models.IntegerField(default=0)
    memory_used = models.FloatField(default=0)
    output = models.TextField()
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
