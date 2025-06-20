from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    github_username = models.CharField(max_length=100, blank=True)
    leetcode_username = models.CharField(max_length=100, blank=True)
    preferred_language = models.CharField(max_length=50, default='python', blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
