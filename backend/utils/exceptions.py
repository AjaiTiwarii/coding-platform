from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class CodeExecutionError(Exception):
    def __init__(self, message, error_type=None, details=None):
        self.message = message
        self.error_type = error_type
        self.details = details
        super().__init__(self.message)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    logger.error(f"API Exception: {exc}", exc_info=True)
    if response is not None:
        response.data = {
            'error': True,
            'message': 'An error occurred',
            'details': response.data,
            'status_code': response.status_code
        }
        return response
    if isinstance(exc, CodeExecutionError):
        return Response({
            'error': True,
            'message': exc.message,
            'error_type': exc.error_type,
            'details': exc.details
        }, status=status.HTTP_400_BAD_REQUEST)
    return Response({
        'error': True,
        'message': 'Internal server error',
        'details': 'An unexpected error occurred'
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
