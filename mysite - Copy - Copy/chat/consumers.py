import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import base64  # For encoding frames

# Dictionary to track the number of connections in each room
room_connections = {}
users = []

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Increment connection count for the room
        if self.room_group_name not in room_connections:
            room_connections[self.room_group_name] = 0
        room_connections[self.room_group_name] += 1

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

        # Send "Connecting..." or "Connected!!" status
        if room_connections[self.room_group_name] == 2:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "chat.status", "status": "Connected!!"},
            )
        else:
            self.send(text_data=json.dumps({"status": "Finding People..."}))

    def disconnect(self, close_code):
        # Decrement connection count for the room
        if self.room_group_name in room_connections:
            room_connections[self.room_group_name] -= 1
            if room_connections[self.room_group_name] <= 0:
                del room_connections[self.room_group_name]

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json.get("type") == "message":
            # Handle chat message
            message = text_data_json.get("message")
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat.message", "message": message}
            )
        elif text_data_json.get("type") == "draw":
            # Handle drawing data
            x = text_data_json.get("X")
            y = text_data_json.get("Y")
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "draw.coordinates", "X": x, "Y": y}
            )
        elif text_data_json.get("type") == "video":
            # Handle video frame
            frame = text_data_json.get("frame")
            sender = text_data_json.get("sender")
            user_N = text_data_json.get("user") 
            if user_N not in users:
                if len(users)==0: # Identify the sender
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name, {"type": "video.frame", "frame": frame, "sender": "local","user":user_N}
                    )
                    users.append(user_N)
                else:
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name, {"type": "video.frame", "frame": frame, "sender": "remote","user":user_N}
                    )
                    users.append(user_N)
            else:
                if user_N == users[0]:
                    async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, {"type": "video.frame", "frame": frame, "sender": "local","user":user_N}
                    )
                else:
                    async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, {"type": "video.frame", "frame": frame, "sender": "remote","user":user_N}
                    )                                       

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))

    def chat_status(self, event):
        status = event["status"]
        self.send(text_data=json.dumps({"status": status}))

    def draw_coordinates(self, event):
        x = event["X"]
        y = event["Y"]
        self.send(text_data=json.dumps({"X": x, "Y": y}))

    def video_frame(self, event):
        frame = event["frame"]
        sender = event["sender"]
        user = event["user"]
        self.send(text_data=json.dumps({"type": "video", "frame": frame, "sender": sender,"user":user}))
