from celery import shared_task
from .models import Submission
from .services import CodeExecutionService

@shared_task
def execute_code_task(submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
        CodeExecutionService.execute_code(submission)
    except Submission.DoesNotExist:
        pass
