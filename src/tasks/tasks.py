from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from .models import Task


@shared_task
def send_task_status_to_websocket(task_id, status):
    # Отримуємо task
    task = Task.objects.get(id=task_id)
    # Створюємо канал для відправки повідомлення через WebSocket
    channel_layer = get_channel_layer()
    room_group_name = f'task_{task_id}'

    # Відправляємо статус в канал (WebSocket)
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            "type": "task_status_update",
            "status": status,
        }
    )