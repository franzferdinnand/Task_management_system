from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tasks.filters import TasksFilter
from tasks.models import Task
from tasks.serializers import TaskSerializer
from tasks.tasks import send_task_status_to_websocket


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_url_kwarg = "task_id"
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TasksFilter

    CACHE_KEY = "tasks_list"
    CACHE_TIMEOUT = 300

    def perform_update(self, serializer):
        """
        Perform the update and check if the status has changed.
        If changed, send the new status to the WebSocket.
        """
        instance = serializer.save()
        if 'status' in serializer.validated_data:
            send_task_status_to_websocket.delay(instance.id, instance.status)

    def list(self, request, *args, **kwargs):
        """
        List all tasks. Use caching to optimize repeated queries.
        """
        page = request.query_params.get('page', 1)
        cache_key = f"{self.CACHE_KEY}_page_{page}"

        tasks = cache.get(cache_key)
        if tasks is None:
            queryset = self.filter_queryset(self.get_queryset())
            paginator = self.paginator
            page_queryset = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page_queryset, many=True)
            tasks = paginator.get_paginated_response(serializer.data).data
            cache.set(cache_key, tasks, self.CACHE_TIMEOUT)

        return Response(tasks)

    def _clear_cache(self):
        cache.delete(self.CACHE_KEY)

    def create(self, request, *args, **kwargs):

        response = super().create(request, *args, **kwargs)
        self._clear_cache()
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        self._clear_cache()
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        self._clear_cache()
        return response
