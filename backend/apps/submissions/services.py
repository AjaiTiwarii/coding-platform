# import os
# import subprocess
# import tempfile
# import logging
# import time

# from .models import Submission, TestCaseResult


# class CodeExecutionService:
#     @staticmethod
#     def execute_submission(submission_id):
#         from .tasks import execute_code_task
#         execute_code_task.delay(submission_id)

#     @staticmethod
#     def execute_code(submission):
#         logger = logging.getLogger(__name__)
#         submission.status = 'RUNNING'
#         submission.save()

#         submission.test_results.all().delete()
#         code = submission.code
#         language = submission.language.name.lower()
#         extension = submission.language.file_extension

#         logger.info(f"Submitted code:\n{code}")

#         test_cases = submission.problem.test_cases.all()
#         passed = 0
#         total_time = 0
#         max_memory = 0
#         test_statuses = []

#         for idx, test_case in enumerate(test_cases, start=1):
#             exec_time = 0
#             output = ''
#             stderr = ''
#             status = 'RUNTIME_ERROR'

#             try:
#                 # this writes code to temp file
#                 with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{extension}', delete=False) as code_file:
#                     code_file.write(code)
#                     code_file_path = code_file.name

#                 logger.info(f"💾 Code written to: {code_file_path}")

#                 # Execute based on language
#                 if language == 'python':
#                     start_time = time.time()
#                     result = subprocess.run(
#                         ['python', code_file_path],
#                         input=test_case.input_data,
#                         text=True,
#                         stdout=subprocess.PIPE,
#                         stderr=subprocess.PIPE,
#                         timeout=submission.problem.time_limit / 1000
#                     )
#                     exec_time = int((time.time() - start_time) * 1000)
#                     output = result.stdout.strip()
#                     stderr = result.stderr.strip()
#                     if result.returncode != 0 or stderr:
#                         status = 'RUNTIME_ERROR'
#                     elif output == test_case.expected_output.strip():
#                         status = 'ACCEPTED'
#                         passed += 1
#                     else:
#                         status = 'WRONG_ANSWER'

#                 elif language == 'c++' or language == 'cpp':
#                     # Compile
#                     binary_path = code_file_path.replace(f".{extension}", "")
#                     compile_proc = subprocess.run(
#                         ['g++', code_file_path, '-o', binary_path],
#                         stdout=subprocess.PIPE,
#                         stderr=subprocess.PIPE
#                     )
#                     if compile_proc.returncode != 0:
#                         stderr = compile_proc.stderr.decode().strip()
#                         status = 'COMPILATION_ERROR'
#                         output = ''
#                     else:
#                         # Run the compiled binary
#                         start_time = time.time()
#                         run_proc = subprocess.run(
#                             [binary_path],
#                             input=test_case.input_data,
#                             text=True,
#                             stdout=subprocess.PIPE,
#                             stderr=subprocess.PIPE,
#                             timeout=submission.problem.time_limit / 1000
#                         )
#                         exec_time = int((time.time() - start_time) * 1000)
#                         output = run_proc.stdout.strip()
#                         stderr = run_proc.stderr.strip()

#                         if run_proc.returncode != 0 or stderr:
#                             status = 'RUNTIME_ERROR'
#                         elif output == test_case.expected_output.strip():
#                             status = 'ACCEPTED'
#                             passed += 1
#                         else:
#                             status = 'WRONG_ANSWER'

#                         # Remove binary
#                         if os.path.exists(binary_path):
#                             os.remove(binary_path)

#                 else:
#                     status = 'COMPILATION_ERROR'
#                     stderr = f"Unsupported language: {language}"

#                 logger.info(f"🔧 Test Case {idx}: output={repr(output)}, expected={repr(test_case.expected_output.strip())}, status={status}")

#             except subprocess.TimeoutExpired:
#                 exec_time = submission.problem.time_limit
#                 status = 'TIME_LIMIT_EXCEEDED'
#                 stderr = 'Time limit exceeded'
#                 output = ''

#             except Exception as e:
#                 status = 'RUNTIME_ERROR'
#                 stderr = str(e)
#                 output = ''

#             # Save result
#             TestCaseResult.objects.create(
#                 submission=submission,
#                 test_case=test_case,
#                 status=status,
#                 execution_time=exec_time,
#                 memory_used=0,
#                 output=output,
#                 error_message=stderr
#             )

#             test_statuses.append(status)
#             total_time += exec_time

#             # Cleanup code file
#             if os.path.exists(code_file_path):
#                 os.remove(code_file_path)

#         # Final verdict
#         submission.test_cases_passed = passed
#         submission.total_test_cases = len(test_cases)
#         submission.execution_time = total_time // len(test_cases) if test_cases else 0
#         submission.memory_used = 0

#         if passed == len(test_cases):
#             submission.status = 'ACCEPTED'
#             submission.score = 100
#         elif 'COMPILATION_ERROR' in test_statuses:
#             submission.status = 'COMPILATION_ERROR'
#             submission.score = 0
#         elif 'RUNTIME_ERROR' in test_statuses:
#             submission.status = 'RUNTIME_ERROR'
#             submission.score = 0
#         elif 'TIME_LIMIT_EXCEEDED' in test_statuses:
#             submission.status = 'TIME_LIMIT_EXCEEDED'
#             submission.score = (passed / len(test_cases)) * 100
#         else:
#             submission.status = 'WRONG_ANSWER'
#             submission.score = (passed / len(test_cases)) * 100

#         submission.save()
#         logger.info(f"Code execution done for submission {submission.id}. Status: {submission.status}")

from .models import Submission, TestCaseResult
from .docker_executor import DockerExecutor
import logging


class CodeExecutionService:
    @staticmethod
    def execute_submission(submission_id):
        from .tasks import execute_code_task
        execute_code_task.delay(submission_id)

    @staticmethod
    def execute_code(submission):
        logger = logging.getLogger(__name__)
        submission.status = 'RUNNING'
        submission.save()

        submission.test_results.all().delete()

        test_cases = submission.problem.test_cases.all()
        passed = 0
        total_time = 0
        test_statuses = []

        executor = DockerExecutor(
            code=submission.code,
            extension=submission.language.file_extension,
            language=submission.language.name
        )

        for test_case in test_cases:
            # Ensure input_data is properly formatted
            input_data = test_case.input_data.strip()
            if not input_data.endswith('\n'):
                input_data += '\n'
            
            output, error, status, exec_time = executor.execute(
                input_data=input_data,
                time_limit_sec=submission.problem.time_limit / 1000
            )

            logger.info(f"Test case input: '{test_case.input_data}'")
            logger.info(f"Output: '{output}', Error: '{error}', Status: '{status}', Exec time: {exec_time}")

            if status == 'SUCCESS':
                # Improved output comparison
                actual_output = output.strip()
                expected_output = test_case.expected_output.strip()
                
                logger.info(f"Actual output: '{actual_output}'")
                logger.info(f"Expected output: '{expected_output}'")
                
                # Compare outputs (handle both string and numeric comparisons)
                if actual_output == expected_output:
                    status = 'ACCEPTED'
                    passed += 1
                else:
                    # Try numeric comparison for cases where formatting might differ
                    try:
                        actual_nums = [float(x) for x in actual_output.split()]
                        expected_nums = [float(x) for x in expected_output.split()]
                        if actual_nums == expected_nums:
                            status = 'ACCEPTED'
                            passed += 1
                        else:
                            status = 'WRONG_ANSWER'
                    except (ValueError, TypeError):
                        # If not numeric, stick with string comparison result
                        status = 'WRONG_ANSWER'
                        
                logger.info(f"Final status for this test case: {status}")

            TestCaseResult.objects.create(
                submission=submission,
                test_case=test_case,
                status=status,
                execution_time=exec_time,
                memory_used=0,
                output=output,
                error_message=error
            )

            test_statuses.append(status)
            total_time += exec_time

        executor.cleanup()

        # Final verdict
        submission.test_cases_passed = passed
        submission.total_test_cases = len(test_cases)
        submission.execution_time = total_time // len(test_cases) if test_cases else 0
        submission.memory_used = 0

        logger.info(f"Passed testcases: {passed} out of {len(test_cases)} total testcases")

        if passed == len(test_cases):
            submission.status = 'ACCEPTED'
            submission.score = 100
        elif 'COMPILATION_ERROR' in test_statuses:
            submission.status = 'COMPILATION_ERROR'
            submission.score = 0
        elif 'RUNTIME_ERROR' in test_statuses:
            submission.status = 'RUNTIME_ERROR'
            submission.score = 0
        elif 'TIME_LIMIT_EXCEEDED' in test_statuses:
            submission.status = 'TIME_LIMIT_EXCEEDED'
            submission.score = (passed / len(test_cases)) * 100
        else:
            submission.status = 'WRONG_ANSWER'
            submission.score = (passed / len(test_cases)) * 100

        submission.save()
        logger.info(f"Code execution completed for submission {submission.id}. Status: {submission.status}, Score: {submission.score}")