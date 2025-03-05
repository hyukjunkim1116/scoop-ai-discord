from . import get_collection
from _datetime import datetime

class ChannelRepository:
    def __init__(self):
        self.collection = get_collection("channels", "channels")

    def create_channel(self, character_name, user_id, channel_id,webhook_url,is_private=True):
        return self.collection.insert_one({
            "character_name": character_name,
            "user_id": user_id,
            "channel_id": channel_id,
            "webhook_url": webhook_url,
            "created_at": datetime.now(),
            "is_private":is_private
        })

    def get_private_channel_by_channel_id(self, channel_id):
        return self.collection.find_one({"channel_id": channel_id})
