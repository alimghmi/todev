from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    owner = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='assigned_projects')
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=1024, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    TODO_CHOICE = 'T'
    INPROGRESS_CHOICE = 'I'
    DONE_CHOICE = 'D'
    STATUS_CHOICES = (
        (TODO_CHOICE, "Todo"),
        (INPROGRESS_CHOICE, "In Progress"),
        (DONE_CHOICE, "Done"),
    )
    
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=1024, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=TODO_CHOICE)
    assignees = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title