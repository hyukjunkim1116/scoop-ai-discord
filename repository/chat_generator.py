from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from .prompt import Prompt
import re


class ChatGenerator:
    def __init__(self):
        load_dotenv()
        self.chat_llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.1,
            max_retries=2
        )
        self.summary_llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.1,
            max_retries=2
        )
    async def generate_summary(self, recent_chats):
        messages = [("system", Prompt.CHAT_SUMMARY.value)]
        # 시스템 프롬프트 먼저 추가
        for chat in recent_chats:
            role = "human" if chat["chat_type"] == "human" else "ai"
            messages.append((role, chat["content"]))
        # 마지막에 요약 요청
        messages.append(("human", "위 대화를 요약해주세요."))
        prompt = ChatPromptTemplate.from_messages(messages) | self.summary_llm | StrOutputParser()
        result = await prompt.ainvoke({})
        print(result,type(result))
        return result

    async def generate_response(self,character, recent_chats, chat_summary, now_chat):

        # Format chat history
        chat_history = ""
        for chat in recent_chats:
            if chat["chat_type"] == "human":
                chat_history += f"human: {chat['content']}\n"
            else:
                chat_history += f"{character.get('character_name', 'Character')}: {chat['content']}\n"
        chat_summary_history = ""
        for summary in chat_summary:
            chat_summary_history+=f"{summary['content']}\n"

        # 1. GENERATE CHAT RESPONSE USING ChatPromptTemplate
        chat_formatted_prompt = Prompt.CHAT.value.format(
            character_name=character.get("character_name", ""),
            intro=character.get("intro", ""),
            gender=character.get("gender", ""),
            mbti=character.get("mbti", ""),
            world_view=character.get("world_view", ""),
            situation=character.get("init_situation", ""),
            secret=character.get("secret", ""),
            chat_summary=chat_summary_history,
            recent_chats=chat_history
        )

        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", chat_formatted_prompt),
            ("human", "{now_chat}")
        ])

        chat_chain = chat_prompt | self.chat_llm | StrOutputParser()
        character_chat = await chat_chain.ainvoke({"now_chat":now_chat})
        character_chat = character_chat.strip()

        situation_formatted_prompt = Prompt.SITUATION.value

        situation_prompt = ChatPromptTemplate.from_messages([
            ("system", situation_formatted_prompt),
            ("human", "{character_chat}")
        ])

        situation_chain = situation_prompt | self.chat_llm | StrOutputParser()
        character_situation = await situation_chain.ainvoke({"character_chat":character_chat})
        character_situation = character_situation.strip()

        # Ensure situation has parentheses
        if not (character_situation.startswith("(") and character_situation.endswith(")")):
            character_situation = f"({character_situation})"

        # 3. GENERATE AFFECTION BASED ON CHAT AND SITUATION
        affection_formatted_prompt = Prompt.AFFECTION.value
        character_situation_chat = f"{character_situation}\n{character_chat}"
        affection_prompt = ChatPromptTemplate.from_messages([
            ("system", affection_formatted_prompt),
            ("human", "{character_situation_chat}")
        ])

        affection_chain = affection_prompt | self.chat_llm | StrOutputParser()
        character_affection = await affection_chain.ainvoke({"character_situation_chat":character_situation_chat})
        character_affection = character_affection.strip()

        # Extract number
        affection_matches = re.findall(r'\d+', character_affection)
        character_affection = int(affection_matches[0]) if affection_matches else int(character.get('init_affection', 50))

        # Limit affection range (0-100)
        character_affection = max(0, min(100, character_affection))
        return character_chat,character_situation,character_affection


