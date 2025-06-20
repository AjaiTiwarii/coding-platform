from django.core.exceptions import ValidationError

def validate_code_length(code):
    if len(code.strip()) < 10:
        raise ValidationError("Code must be at least 10 characters long.")
    if len(code) > 50000:
        raise ValidationError("Code cannot exceed 50,000 characters.")
