from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


app_name = 'authentication'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # path('refresh/', views.refresh_token, name='refresh_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('verify-token/', views.verify_token, name='verify_token'),
    path('dashboard/', views.dashboard_data, name='dashboard'),

]
