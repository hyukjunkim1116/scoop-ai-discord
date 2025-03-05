from . import get_collection
from datetime import datetime
class ChatRepository:
    def __init__(self):
        self.chat_collection = get_collection("chats", "chats")
    def delete_all_by_channel_id(self, channel_id):
        return self.chat_collection.delete_many({"channel_id": channel_id})

    def delete_all(self, user_id):
        return self.chat_collection.delete_many({"user_id": user_id})

    def delete_chats(self, user_id, channel_id, recent_chats):
        return self.chat_collection.delete_many({"user_id": user_id, "channel_id": channel_id, "timestamp": {"$in": [chat["timestamp"] for chat in recent_chats]}})

    def save_chat(self, user_id, channel_id, chat_type, content):
        return self.chat_collection.insert_one({"user_id": user_id, "channel_id": channel_id, "chat_type": chat_type, "content": content, "timestamp": datetime.now()})
    def get_chats_by_channel_id_asc(self, channel_id):
        return list(self.chat_collection.find({"channel_id": channel_id}).sort("timestamp", 1))

