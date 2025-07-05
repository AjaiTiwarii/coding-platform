import os
import subprocess
import tempfile
import shutil
from uuid import uuid4


class DockerExecutor:
    def __init__(self, code: str, extension: str, language: str):
        self.code = code
        self.extension = extension
        self.language = language.lower()
        self.temp_dir = tempfile.mkdtemp()
        self.filename = f"{uuid4().hex}.{self.extension}"
        self.file_path = os.path.join(self.temp_dir, self.filename)
        self._write_code()

    def _write_code(self):
        with open(self.file_path, "w") as f:
            f.write(self.code)

    def execute(self, input_data: str, time_limit_sec: float):
        if self.language == "python":
            return self._run_python(input_data, time_limit_sec)
        elif self.language in ("cpp", "c++"):
            return self._run_cpp(input_data, time_limit_sec)
        else:
            return ("", f"Unsupported language: {self.language}", "COMPILATION_ERROR", 0)

    def _run_python(self, input_data: str, time_limit_sec: float):
        command = [
            "docker", "run", "--rm",
            "-i",
            "--cpus=0.5",
            "--memory=100m",
            "--network=none",
            "-v", f"{self.temp_dir}:/code",
            "python:3.10-slim",
            "python", f"/code/{self.filename}"
        ]
        return self._run_docker_command(command, input_data, time_limit_sec)

    def _run_cpp(self, input_data: str, time_limit_sec: float):
        binary_name = f"{uuid4().hex}"
        binary_path = os.path.join(self.temp_dir, binary_name)

        # Compile inside Docker with better error handling
        compile_cmd = [
            "docker", "run", "--rm",
            "-v", f"{self.temp_dir}:/code",
            "gcc:latest",
            "g++", "-std=c++17", "-Wall", "-O2", "-g", f"/code/{self.filename}", "-o", f"/code/{binary_name}"
        ]

        try:
            compile_proc = subprocess.run(
                compile_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30  # 30 second compile timeout
            )

            if compile_proc.returncode != 0:
                return ("", compile_proc.stderr.decode().strip(), "COMPILATION_ERROR", 0)

            # Run compiled binary with proper stdin handling
            command = [
                "docker", "run", "--rm",
                "-i",
                "--cpus=0.5",
                "--memory=100m",
                "--network=none",
                "-v", f"{self.temp_dir}:/code",
                "gcc:latest",
                "sh", "-c",
                f"echo '{input_data}' | /code/{binary_name}"
            ]

            return self._run_docker_command(command, input_data, time_limit_sec)
        
        except subprocess.TimeoutExpired:
            return ("", "Compilation timeout", "COMPILATION_ERROR", 0)
        except Exception as e:
            return ("", f"Compilation error: {str(e)}", "COMPILATION_ERROR", 0)

    def _run_docker_command(self, command, input_data, time_limit_sec):
        try:
            import time
            start = time.time()
            
            # Ensure input_data ends with newline for proper stdin handling
            if input_data and not input_data.endswith('\n'):
                input_data += '\n'
            
            proc = subprocess.run(
                command,
                input=input_data,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=time_limit_sec
            )
            duration = int((time.time() - start) * 1000)
            
            # Better error handling
            if proc.returncode != 0:
                error_msg = proc.stderr.strip() if proc.stderr.strip() else "Runtime error occurred"
                return (proc.stdout.strip(), error_msg, "RUNTIME_ERROR", duration)
            
            # Check if stderr has warnings but program executed successfully
            if proc.stderr.strip():
                # Log warnings but don't treat as error if returncode is 0
                print(f"Warning: {proc.stderr.strip()}")
            
            return (proc.stdout.strip(), "", "SUCCESS", duration)
            
        except subprocess.TimeoutExpired:
            return ("", "Time limit exceeded", "TIME_LIMIT_EXCEEDED", int(time_limit_sec * 1000))
        except Exception as e:
            return ("", str(e), "RUNTIME_ERROR", 0)

    def cleanup(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)