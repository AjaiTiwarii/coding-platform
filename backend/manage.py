#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

def main():
    """Run administrative tasks."""
    
    # Set default settings module based on environment
    # This supports your settings organization (base.py, development.py, production.py)
    environment = os.environ.get('DJANGO_ENV', 'development')
    
    if environment == 'production':
        default_settings = 'coding_platform.settings.production'
    elif environment == 'testing':
        default_settings = 'coding_platform.settings.testing'
    else:
        default_settings = 'coding_platform.settings.development'
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', default_settings)
    
    # Add the project root to Python path to ensure proper imports
    current_path = Path(__file__).parent.resolve()
    sys.path.insert(0, str(current_path))
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Handle special commands for your coding platform
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        # Custom command shortcuts for development
        if command == 'dev':
            # Shortcut to run development server with custom settings
            sys.argv[1] = 'runserver'
            if len(sys.argv) == 2:
                sys.argv.append('0.0.0.0:8000')
        
        elif command == 'setup':
            # Initial setup command for new installations
            setup_commands = [
                ['makemigrations'],
                ['migrate'],
                ['collectstatic', '--noinput'],
                ['setup_languages'],  # Custom management command for languages
                ['create_sample_problems'],  # Custom management command for sample data
            ]
            
            for cmd in setup_commands:
                print(f"Running: python manage.py {' '.join(cmd)}")
                try:
                    execute_from_command_line(['manage.py'] + cmd)
                except Exception as e:
                    print(f"Warning: Command failed - {e}")
            return
        
        elif command == 'reset_db':
            # Database reset command for development
            if environment == 'development':
                reset_commands = [
                    ['flush', '--noinput'],
                    ['migrate'],
                    ['createsuperuser', '--noinput'] if os.environ.get('DJANGO_SUPERUSER_EMAIL') else ['createsuperuser'],
                ]
                
                for cmd in reset_commands:
                    try:
                        execute_from_command_line(['manage.py'] + cmd)
                    except Exception as e:
                        if 'createsuperuser' not in cmd:
                            print(f"Warning: Command failed - {e}")
            else:
                print("Database reset is only allowed in development environment")
                return
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
