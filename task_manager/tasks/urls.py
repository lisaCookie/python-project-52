# tasks/urls.py

from django.urls import path
from .views import (
    TaskListView, 
    TaskDetailView, 
    TaskCreateView, 
    TaskUpdateView, 
    TaskDeleteView,
    TaskFilterView,
    StatusListView
)

urlpatterns = [
    path('', TaskFilterView.as_view(), name='task-list'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('statuses/', StatusListView.as_view(), name='status_list'),
]
