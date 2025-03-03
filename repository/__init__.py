import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi



load_dotenv()
ca = certifi.where()
client = MongoClient(
    "mongodb+srv://rlagurwns112:1Q87cSAEV9YXym1U@scoop.mmw44.mongodb.net/",
    retryWrites=True,
    w="majority",
    appName="scoop",
    tlsCAFile=ca,
)

def get_collection(database_name:str,collection_name:str):
    return client[database_name][collection_name]

from .user import UserRepository
from .character import CharacterRepository
from .chat import ChatRepository
from .chat_generator import ChatGenerator
from .prompt import Prompt
# from repository import User
#
# # User 클래스 인스턴스 생성
# user_manager = User()
#
# # 메서드 사용
# new_user = {"name": "John", "email": "john@example.com"}
# result = user_manager.create_user(new_user)
