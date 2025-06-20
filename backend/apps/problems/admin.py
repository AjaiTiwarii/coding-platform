from django.contrib import admin
from django.utils.html import format_html
from .models import Problem, Tag, TestCase

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_display', 'problem_count', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    ordering = ['name']
    
    def color_display(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 3px;"></div>',
            obj.color
        )
    color_display.short_description = 'Color'
    
    def problem_count(self, obj):
        return obj.problems.count()
    problem_count.short_description = 'Problems'

class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1
    fields = ['input_data', 'expected_output', 'is_sample', 'is_hidden', 'points', 'order']
    ordering = ['order']

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'difficulty', 'category', 'test_case_count', 
        'is_active', 'created_by', 'created_at'
    ]
    list_filter = ['difficulty', 'category', 'is_active', 'created_at', 'tags']
    search_fields = ['title', 'description', 'category']
    filter_horizontal = ['tags']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TestCaseInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'difficulty', 'category', 'tags')
        }),
        ('Limits & Constraints', {
            'fields': ('time_limit', 'memory_limit', 'constraints')
        }),
        ('Sample Data', {
            'fields': ('sample_input', 'sample_output', 'explanation', 'hints')
        }),
        ('Metadata', {
            'fields': ('created_by', 'is_active'),
            'classes': ('collapse',)
        }),
    )
    
    def test_case_count(self, obj):
        return obj.test_cases.count()
    test_case_count.short_description = 'Test Cases'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by when creating new problem
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = [
        'problem', 'is_sample', 'is_hidden', 'points', 'order', 'created_at'
    ]
    list_filter = ['is_sample', 'is_hidden', 'problem__difficulty', 'created_at']
    search_fields = ['problem__title', 'input_data', 'expected_output']
    ordering = ['problem', 'order']
    
    fieldsets = (
        ('Test Case Data', {
            'fields': ('problem', 'input_data', 'expected_output')
        }),
        ('Configuration', {
            'fields': ('is_sample', 'is_hidden', 'points', 'order')
        }),
    )
