from django.db.models import Q
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from core import models
from core import serializers
from core import permissions


def get_user(pk):
    """
    Helper function to get user either by id or username
    """
    try:
        userobj = models.User.objects.filter(pk=pk)
        if userobj.exists():
            return userobj.first()

    except ValueError:
        userobj = models.User.objects.filter(username=pk)
        if userobj.exists():
            return userobj.first()
        
        return None


class ProjectViewSet(ModelViewSet):
    """
    ViewSet to manage all the operations related to project creation and management
    """
    permission_classes = [permissions.ProjectCustomPermission]
    serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        return models.Project.objects.filter(
            Q(owner=self.request.user) | (
                Q(members__in=[self.request.user]) & Q(is_active=True)
            )).distinct()


    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        user = self.request.query_params.get('user', None)
        project = self.get_object()
        if not user:
            tasks = models.Task.objects.filter(project=project)
        else:
            if user == 'me':
                obj = self.request.user
            else:
                obj = get_user(user)

            if not obj:
                return Response(data={'error': 'provided user doesn\'t exist'},  
                                status=status.HTTP_404_NOT_FOUND)

            tasks = models.Task.objects.filter(project=project, assignees__in=[obj])

        serializer = serializers.ReadTaskSerializer(instance=tasks, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CreateTaskAPI(generics.CreateAPIView):
    """
    APIView to create tasks for a project
    """
    queryset = models.Task.objects.all()
    serializer_class = serializers.CreateTaskSerializer
    permission_classes = [IsAuthenticated]


class DetailTaskAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    APIView to Retrieve, Update and delete a task from a project
    """
    queryset = models.Task.objects.all()
    serializer_class = serializers.UpdateTaskSerializer
    permission_classes = [permissions.TaskCustomPermission]