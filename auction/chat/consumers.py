# import json
# from channels.generic.websocket import WebsocketConsumer
# from channels.consumer import AsyncConsumer
# from channels.db import database_sync_to_async
# from django.contrib.auth import get_user_model
# from asgiref.sync import async_to_sync, sync_to_async
# from django.utils import timezone
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import Message, ChatRoom

# User = get_user_model()

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope['user']
#         self.other_user_id = self.scope['url_route']['kwargs']['other_user_id']
#         self.room_group_name = f'chat_{self.other_user_id}'
#         print("--------------------", self.room_group_name)

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         # accept connection
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )


#     # receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         await self.save_message(message)

#         sender = self.user.username
#         full_name = await self.get_user_full_name(username=sender)
#         print("------------", full_name)
        
#         # send message to WebSocket
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#             'type': 'chat_message',
#             'message': message,
#             'sender': sender,
#             'fullName': full_name,
#             'datetime': timezone.now().isoformat(),
#             }
#         )

#     # receive message from room group
#     async def chat_message(self, event):
#         # send message to WebSocket
#         await self.send(text_data=json.dumps(event))

#     @sync_to_async
#     def get_user(self, user_id):
#         user = User.objects.get(id=user_id)
#         return user
    
#     @sync_to_async
#     def get_user_full_name(self, username):
#         full_name = User.objects.get(username=username).get_user_full_name()
#         print("----------------------", full_name)

#         return full_name

#     @sync_to_async
#     def save_message(self, message):
#         sender = self.user
#         receiver = User.objects.get(id=self.other_user_id)
#         # Assuming there is only one chat room between two users
#         room = ChatRoom.objects.filter(members__in=[sender, receiver]).first()
#         print(room)
#         if not room:
#             room = ChatRoom.objects.create(name=f"Chat between {sender.username} and {receiver.username}")
#             room.members.add(sender, receiver)
#             print(room)

#         msg = Message.objects.create(room=room, sender=sender, message=message)
#         print(msg)

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Message, ChatRoom
from asgiref.sync import async_to_sync, sync_to_async

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.other_user_id = self.scope['url_route']['kwargs']['other_user_id']
        self.room_group_name = self.get_room_group_name(self.user.id, self.other_user_id)
        print(self.room_group_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.user.username
        full_name = await self.get_user_full_name(username=sender)
    
        await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'fullName': full_name,
                'datetime': timezone.now().isoformat(),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    # async def get_user_full_name(self, username):
    #     user = await self.get_user(username)
    #     return user.get_user_full_name()
    
    @sync_to_async
    def get_user_full_name(self, username):
        full_name = User.objects.get(username=username).get_user_full_name()
        print("----------------------", full_name)
        return full_name
    
    @database_sync_to_async
    def get_user(self, user_id):
        print("---------", user_id)
        return User.objects.get(id=user_id)

    async def save_message(self, message):
        sender = self.user
        receiver = await self.get_user(self.other_user_id)
        room_name = self.get_room_group_name(sender.id, receiver.id)

        room, _ = await self.get_or_create_room(sender, receiver, room_name)

        await self.save_message_to_database(room, sender, message)

    @database_sync_to_async
    def save_message_to_database(self, room, sender, message):
        return Message.objects.create(room=room, sender=sender, message=message)

    @staticmethod
    def get_room_group_name(user_id1, user_id2):
        print("--------", user_id1, user_id2)
        sorted_ids = sorted([int(user_id1), int(user_id2)])
        return f'chat_{sorted_ids[0]}_{sorted_ids[1]}'


    @database_sync_to_async
    def get_or_create_room(self, sender, receiver, room_name):
        room, created = ChatRoom.objects.get_or_create(name=room_name)
        if created:
            room.members.add(sender, receiver)
        return room, created
