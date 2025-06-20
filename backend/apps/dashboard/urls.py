from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('overview/', views.dashboard_overview, name='dashboard_overview'),
    path('user-progress/', views.user_progress, name='user_progress'),
    
]