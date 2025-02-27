from . import get_collection

class ChatRepository:
    def __init__(self):
        self.collection = get_collection("chats", "chats")
    def delete_all_by_channel_id(self, channel_id):
        return self.collection.delete_many({"channel_id": channel_id})

    def delete_all(self, user_id):
        return self.collection.delete_many({"user_id": user_id})

