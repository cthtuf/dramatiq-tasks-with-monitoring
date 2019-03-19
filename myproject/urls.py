from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="DramatiqTasksManager API")

urlpatterns = [
    path("", include("dramatiq_tasks_manager.urls")),
    path("schema", schema_view),
] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)  # for swagger
