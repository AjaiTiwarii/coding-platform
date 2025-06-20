from django.contrib import admin
from .models import Submission, TestCaseResult, Language

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'problem', 'language', 'status', 'score', 'submitted_at')
    list_filter = ('status', 'language', 'submitted_at')
    search_fields = ('user__username', 'problem__title')

@admin.register(TestCaseResult)
class TestCaseResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'submission', 'test_case', 'status', 'execution_time', 'memory_used')
    list_filter = ('status',)
    search_fields = ('submission__user__username', 'test_case__input_data')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)