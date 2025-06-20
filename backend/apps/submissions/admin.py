from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count
from .models import Submission, Language, TestCaseResult

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'version', 'file_extension', 'is_active', 
        'time_multiplier', 'memory_multiplier', 'submission_count',
        'judge0_id'  # ✅ Add here to show in list view
    ]
    list_filter = ['is_active', 'name']
    search_fields = ['name', 'version']
    ordering = ['name', 'version']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'version', 'file_extension', 'is_active')
        }),
        ('Execution Configuration', {
            'fields': ('compile_command', 'execute_command')
        }),
        ('Performance Multipliers', {
            'fields': ('time_multiplier', 'memory_multiplier'),
            'description': 'Adjust time and memory limits for this language'
        }),
        ('Judge0 Integration', {
            'fields': ('judge0_id',),  # ✅ Add judge0_id field here
            'description': 'ID used for code execution on Judge0'
        }),
    )

    
    def submission_count(self, obj):
        count = obj.submission_set.count()
        if count > 0:
            url = reverse('admin:submissions_submission_changelist') + f'?language__id={obj.id}'
            return format_html('<a href="{}">{} submissions</a>', url, count)
        return '0 submissions'
    submission_count.short_description = 'Submissions'

class TestCaseResultInline(admin.TabularInline):
    model = TestCaseResult
    extra = 0
    readonly_fields = ['test_case', 'status', 'execution_time', 'memory_used', 'output', 'error_message']
    fields = ['test_case', 'status', 'execution_time', 'memory_used', 'output_preview', 'error_preview']
    
    def output_preview(self, obj):
        if obj.output:
            preview = obj.output[:100] + '...' if len(obj.output) > 100 else obj.output
            return format_html('<pre style="max-width: 300px; overflow: auto;">{}</pre>', preview)
        return '-'
    output_preview.short_description = 'Output Preview'
    
    def error_preview(self, obj):
        if obj.error_message:
            preview = obj.error_message[:100] + '...' if len(obj.error_message) > 100 else obj.error_message
            return format_html('<pre style="max-width: 300px; overflow: auto; color: red;">{}</pre>', preview)
        return '-'
    error_preview.short_description = 'Error Preview'

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user_link', 'problem_link', 'language', 'status_badge', 
        'score', 'execution_time_display', 'memory_used_display', 
        'test_progress', 'submitted_at', 'actions_column'
    ]
    list_filter = [
        'status', 'language', 'problem__difficulty', 'submitted_at', 
        'is_best_submission'
    ]
    search_fields = [
        'user__username', 'user__email', 'problem__title', 
        'language__name', 'code'
    ]
    readonly_fields = [
        'submitted_at', 'judged_at', 'execution_time', 'memory_used',
        'test_cases_passed', 'total_test_cases', 'score'
    ]
    ordering = ['-submitted_at']
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        ('Submission Info', {
            'fields': ('user', 'problem', 'language', 'submitted_at')
        }),
        ('Code', {
            'fields': ('code_preview',),
            'classes': ('collapse',)
        }),
        ('Execution Results', {
            'fields': (
                'status', 'score', 'execution_time', 'memory_used',
                'test_cases_passed', 'total_test_cases', 'judged_at'
            )
        }),
        ('Error Information', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('Flags', {
            'fields': ('is_best_submission',)
        }),
    )
    
    inlines = [TestCaseResultInline]
    
    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    user_link.admin_order_field = 'user__username'
    
    def problem_link(self, obj):
        url = reverse('admin:problems_problem_change', args=[obj.problem.id])
        return format_html('<a href="{}">{}</a>', url, obj.problem.title)
    problem_link.short_description = 'Problem'
    problem_link.admin_order_field = 'problem__title'
    
    def status_badge(self, obj):
        status_colors = {
            'PENDING': '#fbbf24',  # yellow
            'RUNNING': '#3b82f6',  # blue
            'ACCEPTED': '#10b981', # green
            'WRONG_ANSWER': '#ef4444', # red
            'TIME_LIMIT_EXCEEDED': '#f97316', # orange
            'MEMORY_LIMIT_EXCEEDED': '#8b5cf6', # purple
            'COMPILATION_ERROR': '#6b7280', # gray
            'RUNTIME_ERROR': '#dc2626', # dark red
        }
        color = status_colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 4px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def execution_time_display(self, obj):
        if obj.execution_time:
            return f'{obj.execution_time}ms'
        return '-'
    execution_time_display.short_description = 'Time'
    execution_time_display.admin_order_field = 'execution_time'
    
    def memory_used_display(self, obj):
        if obj.memory_used:
            return f'{obj.memory_used:.2f}MB'
        return '-'
    memory_used_display.short_description = 'Memory'
    memory_used_display.admin_order_field = 'memory_used'
    
    def test_progress(self, obj):
        if obj.total_test_cases > 0:
            percentage = (obj.test_cases_passed / obj.total_test_cases) * 100
            color = '#10b981' if percentage == 100 else '#ef4444' if percentage == 0 else '#f97316'
            return format_html(
                '<div style="width: 60px; background-color: #e5e7eb; border-radius: 4px; overflow: hidden;">'
                '<div style="width: {}%; background-color: {}; height: 20px; display: flex; '
                'align-items: center; justify-content: center; color: white; font-size: 10px;">'
                '{}/{}</div></div>',
                percentage, color, obj.test_cases_passed, obj.total_test_cases
            )
        return '-'
    test_progress.short_description = 'Tests'
    
    def code_preview(self, obj):
        if obj.code:
            # Show first 500 characters of code
            preview = obj.code[:500] + '...' if len(obj.code) > 500 else obj.code
            return format_html(
                '<pre style="background-color: #f8fafc; padding: 10px; '
                'border-radius: 4px; overflow: auto; max-height: 300px;">{}</pre>',
                preview
            )
        return 'No code'
    code_preview.short_description = 'Code Preview'
    
    def actions_column(self, obj):
        actions = []
        
        # Rejudge action
        if obj.status in ['WRONG_ANSWER', 'RUNTIME_ERROR', 'TIME_LIMIT_EXCEEDED']:
            actions.append(
                format_html(
                    '<a href="#" onclick="rejudgeSubmission({})" '
                    'style="color: #3b82f6; text-decoration: none; margin-right: 10px;">'
                    '🔄 Rejudge</a>',
                    obj.id
                )
            )
        
        # View details action
        actions.append(
            format_html(
                '<a href="{}" style="color: #10b981; text-decoration: none;">'
                '👁️ Details</a>',
                reverse('admin:submissions_submission_change', args=[obj.id])
            )
        )
        
        return mark_safe(' | '.join(actions))
    actions_column.short_description = 'Actions'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'problem', 'language'
        ).prefetch_related('test_results')
    
    class Media:
        js = ('admin/js/submission_actions.js',)
        css = {
            'all': ('admin/css/submission_admin.css',)
        }

@admin.register(TestCaseResult)
class TestCaseResultAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'submission_link', 'test_case_info', 'status_badge',
        'execution_time_display', 'memory_used_display', 'created_at'
    ]
    list_filter = ['status', 'test_case__is_sample', 'created_at']
    search_fields = [
        'submission__user__username', 'submission__problem__title',
        'test_case__input_data', 'output'
    ]
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Test Case Result', {
            'fields': ('submission', 'test_case', 'status')
        }),
        ('Performance', {
            'fields': ('execution_time', 'memory_used')
        }),
        ('Output & Errors', {
            'fields': ('output_display', 'error_display'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )
    
    def submission_link(self, obj):
        url = reverse('admin:submissions_submission_change', args=[obj.submission.id])
        return format_html('<a href="{}">{}</a>', url, f'#{obj.submission.id}')
    submission_link.short_description = 'Submission'
    submission_link.admin_order_field = 'submission__id'
    
    def test_case_info(self, obj):
        sample_badge = '📝 Sample' if obj.test_case.is_sample else '🔒 Hidden'
        return format_html(
            '{}<br><small>{}</small>',
            sample_badge,
            f'Points: {obj.test_case.points}'
        )
    test_case_info.short_description = 'Test Case'
    
    def status_badge(self, obj):
        status_colors = {
            'ACCEPTED': '#10b981',
            'WRONG_ANSWER': '#ef4444',
            'TIME_LIMIT_EXCEEDED': '#f97316',
            'MEMORY_LIMIT_EXCEEDED': '#8b5cf6',
            'RUNTIME_ERROR': '#dc2626',
        }
        color = status_colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 4px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.status
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def execution_time_display(self, obj):
        return f'{obj.execution_time}ms' if obj.execution_time else '-'
    execution_time_display.short_description = 'Time'
    execution_time_display.admin_order_field = 'execution_time'
    
    def memory_used_display(self, obj):
        return f'{obj.memory_used:.2f}MB' if obj.memory_used else '-'
    memory_used_display.short_description = 'Memory'
    memory_used_display.admin_order_field = 'memory_used'
    
    def output_display(self, obj):
        if obj.output:
            return format_html(
                '<pre style="background-color: #f8fafc; padding: 10px; '
                'border-radius: 4px; overflow: auto; max-height: 200px;">{}</pre>',
                obj.output
            )
        return 'No output'
    output_display.short_description = 'Output'
    
    def error_display(self, obj):
        if obj.error_message:
            return format_html(
                '<pre style="background-color: #fef2f2; padding: 10px; '
                'border-radius: 4px; overflow: auto; max-height: 200px; color: #dc2626;">{}</pre>',
                obj.error_message
            )
        return 'No errors'
    error_display.short_description = 'Error Message'

# Custom admin site configuration
admin.site.site_header = 'CodeMaster Admin'
admin.site.site_title = 'CodeMaster Admin Portal'
admin.site.index_title = 'Welcome to CodeMaster Administration'
