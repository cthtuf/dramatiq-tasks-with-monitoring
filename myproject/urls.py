from django.urls import path, include

urlpatterns = [
    path('', include('dramatiq_tasks_manager.urls')),
]
