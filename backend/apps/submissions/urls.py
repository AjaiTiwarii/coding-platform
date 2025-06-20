from django.urls import path
from . import views

app_name = 'submissions'

urlpatterns = [
    path('languages/', views.LanguageListView.as_view(), name='language-list'),
    path('submit/', views.submit_code, name='submit-code'),
    path('history/', views.user_submissions, name='submission-history'),
    path('<int:pk>/', views.submission_detail, name='submission-detail'),
]