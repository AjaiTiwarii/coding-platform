"""
Settings package initialization.
Automatically imports the appropriate settings based on environment.
"""
import os
from decouple import config

# Determine which settings to use based on environment
DJANGO_ENV = config('DJANGO_ENV', default='development')

if DJANGO_ENV == 'production':
    from .production import *
elif DJANGO_ENV == 'testing':
    from .testing import *
else:
    from .development import *
