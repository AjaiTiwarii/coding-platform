from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
import keyword
import ast

def validate_code_length(code):
    """Validate that code is not too long or too short"""
    if len(code.strip()) < 10:
        raise ValidationError("Code must be at least 10 characters long.")
    
    if len(code) > 50000:  # 50KB limit
        raise ValidationError("Code cannot exceed 50,000 characters.")

def validate_programming_language(language):
    """Validate programming language name"""
    allowed_languages = [
        'python', 'java', 'cpp', 'c', 'javascript', 'typescript',
        'go', 'rust', 'kotlin', 'swift', 'php', 'ruby', 'scala'
    ]
    
    if language.lower() not in allowed_languages:
        raise ValidationError(f"Language '{language}' is not supported.")

def validate_problem_difficulty(difficulty):
    """Validate problem difficulty level"""
    allowed_difficulties = ['EASY', 'MEDIUM', 'HARD']
    
    if difficulty not in allowed_difficulties:
        raise ValidationError(f"Difficulty must be one of: {', '.join(allowed_difficulties)}")

def validate_time_limit(time_limit):
    """Validate execution time limit"""
    if time_limit < 100:  # 100ms minimum
        raise ValidationError("Time limit must be at least 100 milliseconds.")
    
    if time_limit > 10000:  # 10 seconds maximum
        raise ValidationError("Time limit cannot exceed 10 seconds.")

def validate_memory_limit(memory_limit):
    """Validate memory limit"""
    if memory_limit < 16:  # 16MB minimum
        raise ValidationError("Memory limit must be at least 16 MB.")
    
    if memory_limit > 1024:  # 1GB maximum
        raise ValidationError("Memory limit cannot exceed 1024 MB.")

def validate_test_case_input(input_data):
    """Validate test case input data"""
    if len(input_data) > 10000:  # 10KB limit
        raise ValidationError("Test case input cannot exceed 10,000 characters.")

def validate_test_case_output(output_data):
    """Validate test case output data"""
    if len(output_data) > 10000:  # 10KB limit
        raise ValidationError("Test case output cannot exceed 10,000 characters.")

def validate_username_format(username):
    """Validate username format"""
    username_regex = RegexValidator(
        regex=r'^[a-zA-Z0-9_]{3,30}$',
        message='Username must be 3-30 characters long and contain only letters, numbers, and underscores.'
    )
    username_regex(username)
    
    # Check if username is a reserved word
    reserved_words = [
        'admin', 'root', 'user', 'test', 'guest', 'null', 'undefined',
        'api', 'www', 'mail', 'support', 'help', 'about', 'contact'
    ]
    
    if username.lower() in reserved_words:
        raise ValidationError("This username is reserved and cannot be used.")

def validate_problem_slug(slug):
    """Validate problem slug format"""
    slug_regex = RegexValidator(
        regex=r'^[a-z0-9-]+$',
        message='Slug must contain only lowercase letters, numbers, and hyphens.'
    )
    slug_regex(slug)
    
    if len(slug) < 3:
        raise ValidationError("Slug must be at least 3 characters long.")
    
    if len(slug) > 100:
        raise ValidationError("Slug cannot exceed 100 characters.")

def validate_hex_color(color):
    """Validate hex color format"""
    hex_color_regex = RegexValidator(
        regex=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
        message='Color must be a valid hex color (e.g., #FF0000 or #F00).'
    )
    hex_color_regex(color)

def validate_github_username(username):
    """Validate GitHub username format"""
    if not username:
        return  # Optional field
    
    github_regex = RegexValidator(
        regex=r'^[a-zA-Z0-9]([a-zA-Z0-9-]){0,38}$',
        message='Invalid GitHub username format.'
    )
    github_regex(username)

def validate_leetcode_username(username):
    """Validate LeetCode username format"""
    if not username:
        return  # Optional field
    
    leetcode_regex = RegexValidator(
        regex=r'^[a-zA-Z0-9_-]{1,30}$',
        message='Invalid LeetCode username format.'
    )
    leetcode_regex(username)

def validate_python_code_syntax(code):
    """Validate Python code syntax"""
    try:
        ast.parse(code)
    except SyntaxError as e:
        raise ValidationError(f"Python syntax error: {str(e)}")

def validate_submission_frequency(user, time_window=60):
    """Validate submission frequency to prevent spam"""
    from django.utils import timezone
    from datetime import timedelta
    from apps.submissions.models import Submission
    
    recent_time = timezone.now() - timedelta(seconds=time_window)
    recent_submissions = Submission.objects.filter(
        user=user,
        submitted_at__gte=recent_time
    ).count()
    
    if recent_submissions >= 5:  # Max 5 submissions per minute
        raise ValidationError("Too many submissions. Please wait before submitting again.")

def validate_file_size(file):
    """Validate uploaded file size"""
    max_size = 5 * 1024 * 1024  # 5MB
    
    if file.size > max_size:
        raise ValidationError("File size cannot exceed 5MB.")

def validate_image_file(image):
    """Validate uploaded image file"""
    if not image:
        return
    
    validate_file_size(image)
    
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if image.content_type not in allowed_types:
        raise ValidationError("Only JPEG, PNG, GIF, and WebP images are allowed.")

def validate_contest_date_range(start_date, end_date):
    """Validate contest date range"""
    from django.utils import timezone
    
    if start_date >= end_date:
        raise ValidationError("Contest end date must be after start date.")
    
    if start_date < timezone.now():
        raise ValidationError("Contest start date cannot be in the past.")
    
    # Contest duration validation
    duration = end_date - start_date
    if duration.total_seconds() < 3600:  # 1 hour minimum
        raise ValidationError("Contest must be at least 1 hour long.")
    
    if duration.days > 30:  # 30 days maximum
        raise ValidationError("Contest cannot be longer than 30 days.")
