# utils.py - Submission utility functions
import re
from typing import Dict, Any
from .models import Language

class SubmissionUtils:
    @staticmethod
    def detect_language_from_code(code: str) -> str:
        """Detect programming language from code patterns"""
        
        # Python patterns
        if re.search(r'def\s+\w+\s*\(|import\s+\w+|from\s+\w+\s+import|print\s*\(', code):
            return 'python'
        
        # Java patterns
        if re.search(r'public\s+class\s+\w+|public\s+static\s+void\s+main|System\.out\.print', code):
            return 'java'
        
        # C++ patterns
        if re.search(r'#include\s*<.*>|std::|cout\s*<<|cin\s*>>', code):
            return 'cpp'
        
        # C patterns
        if re.search(r'#include\s*<.*\.h>|printf\s*\(|scanf\s*\(', code):
            return 'c'
        
        # JavaScript patterns
        if re.search(r'console\.log\s*\(|function\s+\w+|const\s+\w+\s*=|let\s+\w+\s*=', code):
            return 'javascript'
        
        # Go patterns
        if re.search(r'package\s+main|func\s+main\s*\(|fmt\.Print', code):
            return 'go'
        
        # Rust patterns
        if re.search(r'fn\s+main\s*\(|println!\s*\(|use\s+std::', code):
            return 'rust'
        
        return 'unknown'
    
    @staticmethod
    def validate_code_syntax(code: str, language: Language) -> Dict[str, Any]:
        """Basic syntax validation for code"""
        errors = []
        warnings = []
        
        # Common checks
        if not code.strip():
            errors.append("Code cannot be empty")
            return {'valid': False, 'errors': errors, 'warnings': warnings}
        
        # Language-specific checks
        if language.name.lower() == 'python':
            # Check for basic Python syntax
            if not re.search(r'def\s+\w+|if\s+__name__\s*==\s*["\']__main__["\']', code):
                warnings.append("Consider defining a main function or using if __name__ == '__main__'")
        
        elif language.name.lower() == 'java':
            # Check for main method
            if not re.search(r'public\s+static\s+void\s+main', code):
                errors.append("Java code must contain a main method")
            
            # Check for class definition
            if not re.search(r'public\s+class\s+\w+', code):
                errors.append("Java code must contain a public class")
        
        elif language.name.lower() in ['c', 'cpp']:
            # Check for main function
            if not re.search(r'int\s+main\s*\(', code):
                errors.append("C/C++ code must contain a main function")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    @staticmethod
    def estimate_execution_time(code: str, language: Language) -> int:
        """Estimate execution time based on code complexity"""
        base_time = 100  # Base time in milliseconds
        
        # Count loops and recursive calls
        loop_patterns = [
            r'for\s*\(',
            r'while\s*\(',
            r'do\s*{',
            r'for\s+\w+\s+in\s+',
        ]
        
        loop_count = sum(len(re.findall(pattern, code, re.IGNORECASE)) for pattern in loop_patterns)
        
        # Estimate based on complexity
        estimated_time = base_time + (loop_count * 50)
        
        # Apply language multiplier
        estimated_time = int(estimated_time * language.time_multiplier)
        
        return min(estimated_time, 5000)  # Cap at 5 seconds
    
    @staticmethod
    def format_execution_time(milliseconds: int) -> str:
        """Format execution time for display"""
        if milliseconds < 1000:
            return f"{milliseconds}ms"
        else:
            seconds = milliseconds / 1000
            return f"{seconds:.2f}s"
    
    @staticmethod
    def format_memory_usage(memory_mb: float) -> str:
        """Format memory usage for display"""
        if memory_mb < 1:
            return f"{memory_mb * 1024:.1f}KB"
        else:
            return f"{memory_mb:.2f}MB"
