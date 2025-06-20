# Application-wide constants for the coding platform

# Submission Status Constants
SUBMISSION_STATUS = {
    'PENDING': 'PENDING',
    'RUNNING': 'RUNNING',
    'ACCEPTED': 'ACCEPTED',
    'WRONG_ANSWER': 'WRONG_ANSWER',
    'TIME_LIMIT_EXCEEDED': 'TIME_LIMIT_EXCEEDED',
    'MEMORY_LIMIT_EXCEEDED': 'MEMORY_LIMIT_EXCEEDED',
    'COMPILATION_ERROR': 'COMPILATION_ERROR',
    'RUNTIME_ERROR': 'RUNTIME_ERROR',
    'PRESENTATION_ERROR': 'PRESENTATION_ERROR',
    'SYSTEM_ERROR': 'SYSTEM_ERROR'
}

SUBMISSION_STATUS_CHOICES = [
    (SUBMISSION_STATUS['PENDING'], 'Pending'),
    (SUBMISSION_STATUS['RUNNING'], 'Running'),
    (SUBMISSION_STATUS['ACCEPTED'], 'Accepted'),
    (SUBMISSION_STATUS['WRONG_ANSWER'], 'Wrong Answer'),
    (SUBMISSION_STATUS['TIME_LIMIT_EXCEEDED'], 'Time Limit Exceeded'),
    (SUBMISSION_STATUS['MEMORY_LIMIT_EXCEEDED'], 'Memory Limit Exceeded'),
    (SUBMISSION_STATUS['COMPILATION_ERROR'], 'Compilation Error'),
    (SUBMISSION_STATUS['RUNTIME_ERROR'], 'Runtime Error'),
    (SUBMISSION_STATUS['PRESENTATION_ERROR'], 'Presentation Error'),
    (SUBMISSION_STATUS['SYSTEM_ERROR'], 'System Error'),
]

# Problem Difficulty Constants
DIFFICULTY = {
    'EASY': 'EASY',
    'MEDIUM': 'MEDIUM',
    'HARD': 'HARD'
}

DIFFICULTY_CHOICES = [
    (DIFFICULTY['EASY'], 'Easy'),
    (DIFFICULTY['MEDIUM'], 'Medium'),
    (DIFFICULTY['HARD'], 'Hard'),
]

DIFFICULTY_COLORS = {
    DIFFICULTY['EASY']: '#10B981',    # Green
    DIFFICULTY['MEDIUM']: '#F59E0B',  # Yellow
    DIFFICULTY['HARD']: '#EF4444',   # Red
}

# Programming Languages
SUPPORTED_LANGUAGES = {
    'python': {
        'name': 'Python',
        'version': '3.11',
        'extension': 'py',
        'compile_command': '',
        'execute_command': 'python3 {filename}',
        'mime_type': 'text/x-python'
    },
    'java': {
        'name': 'Java',
        'version': '17',
        'extension': 'java',
        'compile_command': 'javac {filename}',
        'execute_command': 'java {classname}',
        'mime_type': 'text/x-java'
    },
    'cpp': {
        'name': 'C++',
        'version': '17',
        'extension': 'cpp',
        'compile_command': 'g++ -o {output} {filename}',
        'execute_command': './{output}',
        'mime_type': 'text/x-c++src'
    },
    'c': {
        'name': 'C',
        'version': '11',
        'extension': 'c',
        'compile_command': 'gcc -o {output} {filename}',
        'execute_command': './{output}',
        'mime_type': 'text/x-csrc'
    },
    'javascript': {
        'name': 'JavaScript',
        'version': '18',
        'extension': 'js',
        'compile_command': '',
        'execute_command': 'node {filename}',
        'mime_type': 'text/javascript'
    }
}

# Default Limits
DEFAULT_LIMITS = {
    'TIME_LIMIT': 1000,      # milliseconds
    'MEMORY_LIMIT': 256,     # MB
    'CODE_LENGTH_LIMIT': 50000,  # characters
    'TEST_CASE_LIMIT': 100,  # number of test cases
    'SUBMISSION_RATE_LIMIT': 5,  # submissions per minute
}

# File Upload Constants
FILE_UPLOAD = {
    'MAX_FILE_SIZE': 5 * 1024 * 1024,  # 5MB
    'ALLOWED_IMAGE_TYPES': ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
    'PROFILE_PICTURE_SIZE': (200, 200),  # pixels
    'THUMBNAIL_SIZE': (50, 50),  # pixels
}

# Pagination Constants
PAGINATION = {
    'DEFAULT_PAGE_SIZE': 20,
    'MAX_PAGE_SIZE': 100,
    'PROBLEMS_PAGE_SIZE': 25,
    'SUBMISSIONS_PAGE_SIZE': 50,
    'LEADERBOARD_PAGE_SIZE': 100,
}

# Cache Keys and Timeouts
CACHE = {
    'TIMEOUT': {
        'SHORT': 300,        # 5 minutes
        'MEDIUM': 1800,      # 30 minutes
        'LONG': 3600,        # 1 hour
        'VERY_LONG': 86400,  # 24 hours
    },
    'KEYS': {
        'PROBLEM_LIST': 'problems:list:{page}:{filters}',
        'PROBLEM_DETAIL': 'problem:{slug}',
        'USER_STATS': 'user:stats:{user_id}',
        'LEADERBOARD': 'leaderboard:{period}',
        'LANGUAGES': 'languages:active',
    }
}

# Email Templates
EMAIL_TEMPLATES = {
    'WELCOME': 'emails/welcome.html',
    'PASSWORD_RESET': 'emails/password_reset.html',
    'SUBMISSION_RESULT': 'emails/submission_result.html',
    'CONTEST_REMINDER': 'emails/contest_reminder.html',
}

# User Roles and Permissions
USER_ROLES = {
    'STUDENT': 'STUDENT',
    'INSTRUCTOR': 'INSTRUCTOR',
    'ADMIN': 'ADMIN',
    'JUDGE': 'JUDGE',
}

# API Rate Limiting
RATE_LIMITS = {
    'ANONYMOUS': '100/hour',
    'AUTHENTICATED': '1000/hour',
    'SUBMISSION': '60/hour',
    'REGISTRATION': '5/hour',
}

# Contest Constants
CONTEST = {
    'STATUS': {
        'UPCOMING': 'UPCOMING',
        'RUNNING': 'RUNNING',
        'FINISHED': 'FINISHED',
        'CANCELLED': 'CANCELLED',
    },
    'TYPES': {
        'INDIVIDUAL': 'INDIVIDUAL',
        'TEAM': 'TEAM',
    },
    'SCORING': {
        'ACM': 'ACM',
        'IOI': 'IOI',
        'ATCODER': 'ATCODER',
    }
}

# Achievement Constants
ACHIEVEMENTS = {
    'FIRST_SUBMISSION': {
        'name': 'First Steps',
        'description': 'Submit your first solution',
        'icon': '🚀',
        'points': 10,
    },
    'FIRST_ACCEPTED': {
        'name': 'Problem Solver',
        'description': 'Get your first accepted solution',
        'icon': '✅',
        'points': 25,
    },
    'TEN_PROBLEMS': {
        'name': 'Getting Started',
        'description': 'Solve 10 problems',
        'icon': '💡',
        'points': 100,
    },
    'STREAK_WEEK': {
        'name': 'Weekly Warrior',
        'description': 'Solve problems for 7 consecutive days',
        'icon': '🔥',
        'points': 150,
    },
    'CENTURY_CLUB': {
        'name': 'Century Club',
        'description': 'Solve 100 problems',
        'icon': '💯',
        'points': 1000,
    }
}

# Error Messages
ERROR_MESSAGES = {
    'INVALID_CREDENTIALS': 'Invalid email or password.',
    'ACCOUNT_DISABLED': 'Your account has been disabled.',
    'TOKEN_EXPIRED': 'Your session has expired. Please log in again.',
    'PERMISSION_DENIED': 'You do not have permission to perform this action.',
    'RATE_LIMIT_EXCEEDED': 'Too many requests. Please try again later.',
    'FILE_TOO_LARGE': 'File size exceeds the maximum allowed limit.',
    'INVALID_FILE_TYPE': 'File type is not supported.',
    'CODE_TOO_LONG': 'Code exceeds the maximum length limit.',
    'SUBMISSION_FAILED': 'Failed to submit your solution. Please try again.',
}

# Success Messages
SUCCESS_MESSAGES = {
    'REGISTRATION_COMPLETE': 'Account created successfully. Welcome to CodeMaster!',
    'PASSWORD_CHANGED': 'Password updated successfully.',
    'PROFILE_UPDATED': 'Profile updated successfully.',
    'SUBMISSION_QUEUED': 'Solution submitted successfully. Judging in progress...',
    'PROBLEM_CREATED': 'Problem created successfully.',
}

# Logging Configuration
LOG_LEVELS = {
    'DEBUG': 'DEBUG',
    'INFO': 'INFO',
    'WARNING': 'WARNING',
    'ERROR': 'ERROR',
    'CRITICAL': 'CRITICAL',
}

# External API Endpoints
EXTERNAL_APIS = {
    'PISTON': 'https://emkc.org/api/v2/piston',
    'JUDGE0': 'https://api.judge0.com',
}

# Frontend Routes (for email links, etc.)
FRONTEND_ROUTES = {
    'LOGIN': '/auth/login',
    'REGISTER': '/auth/register',
    'DASHBOARD': '/dashboard',
    'PROBLEMS': '/problems',
    'PROBLEM_DETAIL': '/problems/{slug}',
    'SUBMISSIONS': '/submissions',
    'PROFILE': '/profile',
}
