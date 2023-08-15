import base64
import json
import secrets
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile

from user.models import CustomUser
from .models import Message, Conversation
from .serializers import MessageSerializer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("here")
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        chat_type = {"type": "chat_message"}
        sender_id = {"sender_id": self.scope['user'].id}
        return_dict = {**chat_type, **text_data_json, **sender_id}
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            return_dict,
        )

    # Receive message from room group
    def chat_message(self, event):
        text_data_json = event.copy()
        text_data_json.pop("type")
        sender_id = text_data_json.pop("sender_id")
        message, attachment = (
            text_data_json["message"],
            text_data_json.get("attachment"),
        )
        
        if not Conversation.objects.filter(id=int(self.room_name)).exists():
            self.send(
                text_data=json.dumps(
                    {"error" : "conversation has not been found."}
                    )
                )
        
        else:
            self.sendMessage(sender_id ,message, attachment)
    
    def sendMessage(self, sender_id, message, attachment):

        conversation = Conversation.objects.get(id=int(self.room_name))
        if attachment:
            file_str, file_ext = attachment["data"], attachment["format"]
            file_data = ContentFile(
                base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
            )
            _message = Message.objects.create(
                sender = CustomUser.objects.get(id=sender_id),
                attachment=file_data,
                text = message,
                conversation_id=conversation,
            )

        else:
            _message = Message.objects.create(
                sender = CustomUser.objects.get(id=sender_id),
                text = message,
                conversation_id = conversation,
            )

        serializer = MessageSerializer(instance=_message)

        self.send(
            text_data=json.dumps(
            serializer.data
            )
        )