# task_manager/urls.py


from django.contrib import admin
from django.urls import path
from task_manager.views import IndexView, CustomLoginView, CustomLogoutView
from django.urls import path, include

urlpatterns = [
    path("", IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('users/', include('task_manager.users.urls')),  # убрали префикс task_manager
    path('tasks/', include('task_manager.tasks.urls')),  # убрали префикс task_manager
    path('labels/', include('task_manager.labels.urls')),  # убрали префикс task_manager
    path('statuses/', include('task_manager.statuses.urls')), 
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
