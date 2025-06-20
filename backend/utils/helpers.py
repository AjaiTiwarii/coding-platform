import hashlib
import random
import string
import re
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.utils.text import slugify
from django.core.mail import send_mail
from django.template.loader import render_to_string
import json
import logging

logger = logging.getLogger(__name__)

def generate_random_string(length=32, include_numbers=True, include_symbols=False):
    """Generate a random string of specified length"""
    characters = string.ascii_letters
    
    if include_numbers:
        characters += string.digits
    
    if include_symbols:
        characters += "!@#$%^&*"
    
    return ''.join(random.choice(characters) for _ in range(length))

def generate_problem_slug(title):
    """Generate a unique slug for a problem"""
    base_slug = slugify(title)
    
    # If slug already exists, append a number
    from apps.problems.models import Problem
    counter = 1
    unique_slug = base_slug
    
    while Problem.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{base_slug}-{counter}"
        counter += 1
    
    return unique_slug

def hash_code(code):
    """Generate hash for code to detect duplicates"""
    # Normalize code by removing extra whitespace and comments
    normalized_code = re.sub(r'\s+', ' ', code.strip())
    normalized_code = re.sub(r'#.*', '', normalized_code)  # Remove Python comments
    normalized_code = re.sub(r'//.*', '', normalized_code)  # Remove C++/Java comments
    
    return hashlib.md5(normalized_code.encode()).hexdigest()

def calculate_execution_score(execution_time, time_limit, memory_used, memory_limit):
    """Calculate performance score based on execution time and memory usage"""
    time_score = max(0, (time_limit - execution_time) / time_limit * 50)
    memory_score = max(0, (memory_limit - memory_used) / memory_limit * 50)
    
    return min(100, time_score + memory_score)

def format_time_duration(milliseconds):
    """Format execution time in a human-readable format"""
    if milliseconds < 1000:
        return f"{milliseconds}ms"
    elif milliseconds < 60000:
        seconds = milliseconds / 1000
        return f"{seconds:.2f}s"
    else:
        minutes = milliseconds // 60000
        seconds = (milliseconds % 60000) / 1000
        return f"{minutes}m {seconds:.2f}s"

def format_memory_size(bytes_amount):
    """Format memory size in a human-readable format"""
    if bytes_amount < 1024:
        return f"{bytes_amount}B"
    elif bytes_amount < 1024 * 1024:
        kb = bytes_amount / 1024
        return f"{kb:.2f}KB"
    elif bytes_amount < 1024 * 1024 * 1024:
        mb = bytes_amount / (1024 * 1024)
        return f"{mb:.2f}MB"
    else:
        gb = bytes_amount / (1024 * 1024 * 1024)
        return f"{gb:.2f}GB"

def get_difficulty_color(difficulty):
    """Get color code for problem difficulty"""
    from .constants import DIFFICULTY_COLORS
    return DIFFICULTY_COLORS.get(difficulty, '#6B7280')

def calculate_user_rating(user):
    """Calculate user rating based on problem solving history"""
    from apps.submissions.models import Submission
    from apps.problems.models import Problem
    
    # Get user's accepted submissions
    accepted_submissions = Submission.objects.filter(
        user=user,
        status='ACCEPTED'
    ).select_related('problem')
    
    total_score = 0
    problem_count = 0
    
    for submission in accepted_submissions:
        difficulty = submission.problem.difficulty
        
        # Scoring based on difficulty
        if difficulty == 'EASY':
            score = 10
        elif difficulty == 'MEDIUM':
            score = 25
        elif difficulty == 'HARD':
            score = 50
        else:
            score = 0
        
        # Bonus for execution time and memory efficiency
        time_bonus = max(0, (submission.problem.time_limit - submission.execution_time) / submission.problem.time_limit * 5)
        memory_bonus = max(0, (submission.problem.memory_limit - submission.memory_used) / submission.problem.memory_limit * 5)
        
        total_score += score + time_bonus + memory_bonus
        problem_count += 1
    
    # Calculate average score and apply multiplier
    if problem_count > 0:
        average_score = total_score / problem_count
        rating = int(average_score * problem_count * 0.1)  # Scale to reasonable range
        return min(3000, max(0, rating))  # Cap between 0-3000
    
    return 0

def send_notification_email(user, subject, template, context=None):
    """Send notification email to user"""
    if not context:
        context = {}
    
    context.update({
        'user': user,
        'site_name': getattr(settings, 'SITE_NAME', 'CodeMaster'),
        'site_url': getattr(settings, 'SITE_URL', 'http://localhost:3000')
    })
    
    try:
        html_message = render_to_string(template, context)
        
        send_mail(
            subject=subject,
            message='',  # Plain text version (can be improved)
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )
        
        logger.info(f"Email sent to {user.email}: {subject}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {user.email}: {str(e)}")
        return False

def cache_key_generator(prefix, *args, **kwargs):
    """Generate cache key with consistent format"""
    key_parts = [prefix]
    
    # Add positional arguments
    for arg in args:
        key_parts.append(str(arg))
    
    # Add keyword arguments (sorted for consistency)
    for key, value in sorted(kwargs.items()):
        key_parts.append(f"{key}:{value}")
    
    return ":".join(key_parts)

def get_cached_or_set(cache_key, callable_func, timeout=3600):
    """Get value from cache or set it using callable function"""
    value = cache.get(cache_key)
    
    if value is None:
        value = callable_func()
        cache.set(cache_key, value, timeout)
    
    return value

def paginate_queryset(queryset, page_number, page_size=20):
    """Paginate a queryset and return page info"""
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    
    paginator = Paginator(queryset, page_size)
    
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    
    return {
        'objects': page.object_list,
        'has_next': page.has_next(),
        'has_previous': page.has_previous(),
        'current_page': page.number,
        'total_pages': paginator.num_pages,
        'total_count': paginator.count,
        'page_size': page_size
    }

def sanitize_filename(filename):
    """Sanitize filename for safe storage"""
    # Remove or replace dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        max_name_length = 255 - len(ext) - 1
        filename = f"{name[:max_name_length]}.{ext}" if ext else name[:255]
    
    return filename

def extract_code_metrics(code, language):
    """Extract basic metrics from code"""
    lines = code.split('\n')
    
    metrics = {
        'total_lines': len(lines),
        'non_empty_lines': len([line for line in lines if line.strip()]),
        'comment_lines': 0,
        'character_count': len(code),
        'estimated_complexity': 'LOW'
    }
    
    # Count comments based on language
    comment_patterns = {
        'python': r'#.*',
        'java': r'//.*|/\*.*?\*/',
        'cpp': r'//.*|/\*.*?\*/',
        'c': r'//.*|/\*.*?\*/',
        'javascript': r'//.*|/\*.*?\*/'
    }
    
    if language.lower() in comment_patterns:
        pattern = comment_patterns[language.lower()]
        for line in lines:
            if re.search(pattern, line):
                metrics['comment_lines'] += 1
    
    # Estimate complexity based on control structures
    complexity_keywords = ['if', 'else', 'while', 'for', 'switch', 'case', 'try', 'catch']
    complexity_count = sum(len(re.findall(rf'\b{keyword}\b', code, re.IGNORECASE)) for keyword in complexity_keywords)
    
    if complexity_count > 20:
        metrics['estimated_complexity'] = 'HIGH'
    elif complexity_count > 10:
        metrics['estimated_complexity'] = 'MEDIUM'
    
    return metrics

def is_rate_limited(user, action, limit_per_hour=60):
    """Check if user is rate limited for a specific action"""
    cache_key = f"rate_limit:{user.id}:{action}:{timezone.now().hour}"
    current_count = cache.get(cache_key, 0)
    
    if current_count >= limit_per_hour:
        return True
    
    # Increment counter
    cache.set(cache_key, current_count + 1, 3600)  # 1 hour timeout
    return False

def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_user_action(user, action, details=None):
    """Log user action for audit trail"""
    log_data = {
        'user_id': user.id if user else None,
        'username': user.username if user else 'Anonymous',
        'action': action,
        'timestamp': timezone.now().isoformat(),
        'details': details or {}
    }
    
    logger.info(f"User Action: {json.dumps(log_data)}")

def clean_output(output):
    """Clean output string for display"""
    # Remove extra whitespace and normalize line endings
    cleaned = re.sub(r'\r\n|\r', '\n', output)
    cleaned = cleaned.strip()
    
    # Limit output length to prevent abuse
    max_length = 10000
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length] + "\n... (output truncated)"
    
    return cleaned

def generate_api_key():
    """Generate API key for external integrations"""
    return f"ck_{generate_random_string(32)}"

def validate_json_format(json_string):
    """Validate and parse JSON string"""
    try:
        return json.loads(json_string), None
    except json.JSONDecodeError as e:
        return None, str(e)
