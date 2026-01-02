# labels/urls.py

from django.urls import path
from .views import LabelListView, LabelCreateView, LabelUpdateView, LabelDeleteView

urlpatterns = [
    path('', LabelListView.as_view(), name='label-list'),
    path('create/', LabelCreateView.as_view(), name='label-create'),
    path('<int:pk>/update/', LabelUpdateView.as_view(), name='label-update'),
    path('<int:pk>/delete/', LabelDeleteView.as_view(), name='label-delete'),
]