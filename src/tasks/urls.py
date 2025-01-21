from rest_framework.routers import DefaultRouter

from tasks.api import TaskViewSet


router = DefaultRouter()
router.register("", viewset=TaskViewSet)

urlpatterns = [] + router.urls
