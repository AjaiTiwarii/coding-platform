from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Main dashboard endpoints [19][20]
    path('overview/', views.dashboard_overview, name='dashboard_overview'),
    path('recent-activity/', views.recent_activity, name='recent_activity'),
    path('user-progress/', views.user_progress, name='user_progress'),
    
    # Statistics endpoints [7][13]
    path('stats/problems/', views.problem_statistics, name='problem_statistics'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    
    # Additional dashboard endpoints for extended functionality [18]
    path('achievements/', views.user_achievements, name='user_achievements'),
    path('weekly-stats/', views.weekly_statistics, name='weekly_statistics'),
    path('language-stats/', views.language_statistics, name='language_statistics'),
    path('submission-heatmap/', views.submission_heatmap, name='submission_heatmap'),
]
