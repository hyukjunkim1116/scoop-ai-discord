from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from .prompt import Prompt
from langchain.chains import ConversationChain


class ChatGenerator:
    def __init__(self):
        load_dotenv()
        self.chat_llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.1,
            max_retries=2
        )

    async def generate_public_response(self, character_name, now_chat):
        character_system_prompt = Prompt.CHARACTER_PUBLIC_MAP.value[character_name]
        prompt = ChatPromptTemplate.from_messages([
            ("system", character_system_prompt),
            ("human", "{now_chat}")
        ])
        chain = prompt | self.chat_llm | StrOutputParser()
        result = await chain.ainvoke({"now_chat": now_chat})
        return result


