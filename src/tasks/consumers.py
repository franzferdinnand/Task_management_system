import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from tasks.models import Task


class TaskConsumer(AsyncWebsocketConsumer):
    """
    Websocket consumer for task status updates.
    The consumer is connected to a specific task and listens for status updates.
    """
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.room_name = f"task_{self.task_id}"
        self.room_group_name = f"task_{self.task_id}"

        # Check if the task exists
        task = await database_sync_to_async(Task.objects.get)(id=self.task_id)

        if task:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_task_status(self, status):
        await self.send(text_data=json.dumps({
            'status': status
        }))
