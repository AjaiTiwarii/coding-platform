# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views

# app_name = 'submissions'

# router = DefaultRouter()
# router.register(r'submissions', views.SubmissionViewSet, basename='submission')

# urlpatterns = [
#     path('', include(router.urls)),

#     # ✅ Custom API endpoints
#     path('submit/', views.submit_code, name='submit_code'),  # ✅ your new POST endpoint
#     path('history/', views.user_submissions, name='user_submissions'),

#     # Languages
#     path('languages/', views.LanguageListView.as_view(), name='language-list'),
#     path('languages/<int:pk>/', views.LanguageDetailView.as_view(), name='language-detail'),

#     # Submission management
#     path('submissions/<int:submission_id>/result/', views.SubmissionResultView.as_view(), name='submission-result'),
#     path('submissions/<int:submission_id>/rejudge/', views.RejudgeSubmissionView.as_view(), name='submission-rejudge'),
#     path('submissions/<int:submission_id>/status/', views.SubmissionStatusView.as_view(), name='submission-status'),

#     # User & Problem submissions
#     path('my-submissions/', views.MySubmissionListView.as_view(), name='my-submissions'),
#     path('users/<int:user_id>/submissions/', views.UserSubmissionListView.as_view(), name='user-submissions'),
#     path('problems/<int:problem_id>/submissions/', views.ProblemSubmissionListView.as_view(), name='problem-submissions'),

#     # Stats
#     path('stats/', views.SubmissionStatsView.as_view(), name='submission-stats'),
#     path('leaderboard/', views.LeaderboardView.as_view(), name='submission-leaderboard'),
# ]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'submissions'

# Router for ViewSet-based views
router = DefaultRouter()
router.register(r'submissions', views.SubmissionViewSet, basename='submission')

urlpatterns = [
    # RESTful endpoints for SubmissionViewSet
    path('', include(router.urls)),

    # ✅ Custom code submission & history
    path('submit/', views.submit_code, name='submit_code'),
    path('history/', views.user_submissions, name='user_submissions'),

    # ✅ Language management
    path('languages/', views.LanguageListView.as_view(), name='language-list'),
    path('languages/<int:pk>/', views.LanguageDetailView.as_view(), name='language-detail'),

    # ✅ Individual submission management
    path('submissions/<int:submission_id>/result/', views.SubmissionResultView.as_view(), name='submission-result'),
    path('submissions/<int:submission_id>/rejudge/', views.RejudgeSubmissionView.as_view(), name='submission-rejudge'),
    path('submissions/<int:submission_id>/status/', views.SubmissionStatusView.as_view(), name='submission-status'),

    # ✅ User-specific endpoints
    path('my-submissions/', views.MySubmissionListView.as_view(), name='my-submissions'),
    path('users/<int:user_id>/submissions/', views.UserSubmissionListView.as_view(), name='user-submissions'),

    # ✅ Problem-specific
    path('problems/<int:problem_id>/submissions/', views.ProblemSubmissionListView.as_view(), name='problem-submissions'),

    # ✅ Submission analytics
    path('stats/', views.SubmissionStatsView.as_view(), name='submission-stats'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='submission-leaderboard'),
]
