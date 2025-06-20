from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.http import Http404
import logging

logger = logging.getLogger(__name__)

class CodeExecutionError(Exception):
    """Raised when code execution fails"""
    def __init__(self, message, error_type=None, details=None):
        self.message = message
        self.error_type = error_type
        self.details = details
        super().__init__(self.message)

class CompilationError(CodeExecutionError):
    """Raised when code compilation fails"""
    pass

class TimeoutError(CodeExecutionError):
    """Raised when code execution times out"""
    pass

class MemoryLimitError(CodeExecutionError):
    """Raised when code exceeds memory limit"""
    pass

class ProblemNotFoundError(Exception):
    """Raised when a problem is not found"""
    pass

class InvalidSubmissionError(Exception):
    """Raised when submission data is invalid"""
    pass

class TestCaseError(Exception):
    """Raised when test case execution fails"""
    def __init__(self, message, test_case_id=None, expected=None, actual=None):
        self.test_case_id = test_case_id
        self.expected = expected
        self.actual = actual
        super().__init__(message)

class LanguageNotSupportedError(Exception):
    """Raised when programming language is not supported"""
    pass

class RateLimitError(Exception):
    """Raised when user exceeds submission rate limit"""
    pass

class InsufficientPermissionsError(Exception):
    """Raised when user lacks required permissions"""
    pass

def custom_exception_handler(exc, context):
    """
    Custom exception handler for the API.
    Provides consistent error response format.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Log the exception
    logger.error(f"API Exception: {exc}", exc_info=True)
    
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': 'An error occurred',
            'details': response.data,
            'status_code': response.status_code
        }
        response.data = custom_response_data
        return response
    
    # Handle custom exceptions
    if isinstance(exc, CodeExecutionError):
        return Response({
            'error': True,
            'message': exc.message,
            'error_type': exc.error_type,
            'details': exc.details
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif isinstance(exc, ProblemNotFoundError):
        return Response({
            'error': True,
            'message': 'Problem not found',
            'details': str(exc)
        }, status=status.HTTP_404_NOT_FOUND)
    
    elif isinstance(exc, InvalidSubmissionError):
        return Response({
            'error': True,
            'message': 'Invalid submission data',
            'details': str(exc)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif isinstance(exc, TestCaseError):
        return Response({
            'error': True,
            'message': 'Test case execution failed',
            'test_case_id': exc.test_case_id,
            'expected': exc.expected,
            'actual': exc.actual,
            'details': str(exc)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif isinstance(exc, LanguageNotSupportedError):
        return Response({
            'error': True,
            'message': 'Programming language not supported',
            'details': str(exc)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif isinstance(exc, RateLimitError):
        return Response({
            'error': True,
            'message': 'Rate limit exceeded',
            'details': str(exc)
        }, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    elif isinstance(exc, InsufficientPermissionsError):
        return Response({
            'error': True,
            'message': 'Insufficient permissions',
            'details': str(exc)
        }, status=status.HTTP_403_FORBIDDEN)
    
    elif isinstance(exc, ValidationError):
        return Response({
            'error': True,
            'message': 'Validation error',
            'details': exc.message_dict if hasattr(exc, 'message_dict') else str(exc)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif isinstance(exc, Http404):
        return Response({
            'error': True,
            'message': 'Resource not found',
            'details': str(exc)
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Handle unexpected exceptions
    return Response({
        'error': True,
        'message': 'Internal server error',
        'details': 'An unexpected error occurred'
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
