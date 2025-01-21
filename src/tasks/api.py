from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from tasks.tasks import send_task_status_to_websocket
from tasks.filters import TasksFilter
from tasks.models import Task
from tasks.serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_url_kwarg = "task_id"
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TasksFilter

    def perform_update(self, serializer):
        instance = serializer.save()

        # Check if the status has changed
        if 'status' in serializer.validated_data:
            send_task_status_to_websocket.delay(instance.id, instance.status)
