from . import get_collection
from _datetime import datetime
class CharacterRepository:
    def __init__(self):
        self.collection = get_collection("characters", "characters")

    def initialize_character(self, character_name, user_id, channel_id,webhook_url):
        return self.collection.insert_one({
            "character_name": character_name,
            "user_id": user_id,
            "channel_id": channel_id,
            "webhook_url": webhook_url,
            "created_at": datetime.now(),
            "character_image_url": None,
        })

    def get_character_by_channel_id(self, channel_id):
        return self.collection.find_one({"channel_id": channel_id})

    def update_character(self, character_id, update_data):
        return self.collection.update_one(
            {"_id": character_id},
            {"$set": update_data}
        )

    def delete_all(self, user_id):
        return self.collection.delete_many({"user_id": user_id})

    def get_characters_by_user_id(self, user_id):
        return list(self.collection.find({"user_id": user_id}))
# 성별 gender
# 소개 intro
# mbti mbti
# 시작호감도 start_affection
# 세계관 world_view
# 첫메세지 first_chat
# 처음상황 first_situation
# 비밀 secret
# 이미지프롬프트 image_prompt
# 확인 confirm
# 시작