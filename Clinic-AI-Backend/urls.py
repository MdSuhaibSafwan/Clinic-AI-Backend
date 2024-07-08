from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from ai.api.views import AssistantViewSet

router = routers.DefaultRouter()
router.register(r"assistant", AssistantViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("ai.api.urls")),
    path("", include(router.urls)),
] 
