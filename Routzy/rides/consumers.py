import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the room name from the URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'  # Group name for the room

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,  # Group to join
            self.channel_name  # Channel name (unique for each WebSocket connection)
        )
        await self.accept()  # Accept the WebSocket connection

    async def disconnect(self, close_code):
        # Leave the room group when the WebSocket is closed
        await self.channel_layer.group_discard(
            self.room_group_name,  # Group to leave
            self.channel_name  # Channel to discard
        )

    async def receive(self, text_data):
        # Handle receiving a message from the WebSocket
        data = json.loads(text_data)  # Parse the received JSON message
        sender = data['sender']  # Extract sender name
        message = data['message']  # Extract message content

        # Save the message to the database
        Message.objects.create(sender=sender, content=message)

        # Send the message to the room group (broadcast to all connected clients in the room)
        await self.channel_layer.group_send(
            self.room_group_name,  # The room group to send the message to
            {
                'type': 'chat_message',  # Message type (you define this handler below)
                'sender': sender,  # Sender name
                'message': message  # Message content
            }
        )

    async def chat_message(self, event):
        # Handle receiving a message from the room group (broadcast)
        sender = event['sender']
        message = event['message']

        # Send the message to the WebSocket (client)
        await self.send(text_data=json.dumps({
            'sender': sender,  # Sender name
            'message': message  # Message content
        }))
