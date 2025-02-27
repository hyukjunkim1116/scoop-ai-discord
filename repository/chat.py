from . import get_collection
from datetime import datetime
class ChatRepository:
    def __init__(self):
        self.chat_collection = get_collection("chats", "chats")
        self.summary_collection = get_collection("chats", "summaries")
    def delete_all_by_channel_id(self, channel_id):
        return self.chat_collection.delete_many({"channel_id": channel_id})

    def delete_all(self, user_id):
        return self.chat_collection.delete_many({"user_id": user_id})

    def get_recent_chats_asc(self, user_id, channel_id):
        return list(self.chat_collection.find({"user_id": user_id, "channel_id": channel_id}).sort("timestamp", 1))

    def get_chat_summary_asc(self, user_id, channel_id):
        return list(self.summary_collection.find({"user_id": user_id, "channel_id": channel_id}).sort("timestamp", 1))

    def delete_chats(self, user_id, channel_id, recent_chats):
        return self.chat_collection.delete_many({"user_id": user_id, "channel_id": channel_id, "timestamp": {"$in": [chat["timestamp"] for chat in recent_chats]}})

    def save_chat(self, user_id, channel_id, chat_type, content,affection=None):
        return self.chat_collection.insert_one({"user_id": user_id, "channel_id": channel_id, "chat_type": chat_type, "content": content, "timestamp": datetime.now(),"affection":affection})

    def save_summary(self, user_id, channel_id, new_chat_summary):
        return self.summary_collection.insert_one({"user_id": user_id, "channel_id": channel_id, "summary": new_chat_summary, "timestamp": datetime.now()})

