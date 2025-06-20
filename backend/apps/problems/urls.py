from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'problems'

router = DefaultRouter()
router.register(r'problems', views.ProblemViewSet, basename='problem')

urlpatterns = [
    path('', include(router.urls)),
    
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    

    path('', views.problem_list, name='problem_list'),
]
