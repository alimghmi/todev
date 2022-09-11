from django.urls import path, include

from user import views


urlpatterns = [
    path('', view=views.CreateUserView.as_view(), name='signup-api')
]
