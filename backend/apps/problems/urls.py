from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'problems'

router = DefaultRouter()
router.register(r'problems', views.ProblemViewSet, basename='problem')

urlpatterns = [
    path('', include(router.urls)),
    path('tags/', views.TagListView.as_view(), name='tag-list'),
    path('tags/<int:pk>/', views.TagDetailView.as_view(), name='tag-detail'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('problems/<int:problem_id>/test-cases/', views.TestCaseListView.as_view(), name='test-case-list'),
    path('problems/<slug:slug>/', views.ProblemBySlugView.as_view(), name='problem-by-slug'),
    path('stats/', views.ProblemStatsView.as_view(), name='problem-stats'),

    path('', views.problem_list, name='problem_list'),
]
