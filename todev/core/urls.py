from django.urls import path, include
from rest_framework import routers

from core import views

router = routers.SimpleRouter()
router.register('projects', views.ProjectViewSet, basename='project')

urlpatterns = router.urls

urlpatterns += [
    path('tasks/', views.CreateTaskAPI.as_view(), name='create-task'),
    path('tasks/<pk>/', views.DetailTaskAPI.as_view(), name='detail-task'),
]
