import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)

def get_collection(database_name:str,collection_name:str):
    return client[database_name][collection_name]

from v2.repository.chat import ChatRepository
from v2.repository.chat_generator import ChatGenerator
from v2.repository.prompt import Prompt
from v2.repository.channel import ChannelRepository
from v2.repository.context_chat_generator import ContextChatGenerator
