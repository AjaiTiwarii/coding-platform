from django.core.management.base import BaseCommand
from apps.submissions.models import Language

class Command(BaseCommand):
    help = 'Setup default programming languages'
    
    def handle(self, *args, **options):
        languages = [
            {
                'name': 'Python',
                'version': '3.10.0',
                'file_extension': 'py',
                'compile_command': '',
                'execute_command': 'python3 {file}',
                'time_multiplier': 3.0,
                'memory_multiplier': 2.0,
            },
            {
                'name': 'Java',
                'version': '15.0.2',
                'file_extension': 'java',
                'compile_command': 'javac {file}',
                'execute_command': 'java {class}',
                'time_multiplier': 2.0,
                'memory_multiplier': 2.5,
            },
            {
                'name': 'C++',
                'version': '10.2.0',
                'file_extension': 'cpp',
                'compile_command': 'g++ -o {executable} {file}',
                'execute_command': './{executable}',
                'time_multiplier': 1.0,
                'memory_multiplier': 1.0,
            },
            {
                'name': 'C',
                'version': '10.2.0',
                'file_extension': 'c',
                'compile_command': 'gcc -o {executable} {file}',
                'execute_command': './{executable}',
                'time_multiplier': 1.0,
                'memory_multiplier': 1.0,
            },
            {
                'name': 'JavaScript',
                'version': '18.15.0',
                'file_extension': 'js',
                'compile_command': '',
                'execute_command': 'node {file}',
                'time_multiplier': 2.5,
                'memory_multiplier': 2.0,
            },
            {
                'name': 'Go',
                'version': '1.16.2',
                'file_extension': 'go',
                'compile_command': 'go build {file}',
                'execute_command': './{executable}',
                'time_multiplier': 1.5,
                'memory_multiplier': 1.5,
            },
            {
                'name': 'Rust',
                'version': '1.68.2',
                'file_extension': 'rs',
                'compile_command': 'rustc {file}',
                'execute_command': './{executable}',
                'time_multiplier': 1.2,
                'memory_multiplier': 1.3,
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for lang_data in languages:
            language, created = Language.objects.get_or_create(
                name=lang_data['name'],
                version=lang_data['version'],
                defaults=lang_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created language: {language.name} {language.version}'
                    )
                )
            else:
                # Update existing language
                for key, value in lang_data.items():
                    setattr(language, key, value)
                language.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'Updated language: {language.name} {language.version}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Setup complete! Created: {created_count}, Updated: {updated_count}'
            )
        )
