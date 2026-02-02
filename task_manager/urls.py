# task_manager/urls.py


from django.contrib import admin
from django.urls import path, include
from task_manager.views import IndexView

urlpatterns = [
    path("", IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('users/', include('task_manager.users.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
]

