from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Problem, Tag
from .serializers import ProblemSerializer, ProblemDetailSerializer, TagSerializer
from .serializers import TestCaseSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def problem_list(request):
    problems = Problem.objects.all()
    serializer = ProblemSerializer(problems, many=True)
    return Response(serializer.data)



class ProblemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Problem.objects.filter(is_active=True)
    serializer_class = ProblemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['difficulty', 'category', 'tags']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title', 'difficulty']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProblemDetailSerializer
        return ProblemSerializer
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        categories = Problem.objects.values_list('category', flat=True).distinct()
        return Response(list(categories))
    
    @action(detail=False, methods=['get'])
    def tags(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)




class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        categories = Problem.objects.filter(is_active=True).values_list('category', flat=True).distinct()
        return Response(list(categories))
