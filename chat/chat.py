from langchain_openai import ChatOpenAI
from chat.nagisa_kazuki import get_parameters as get_nagisa_parameters
from chat.nagisa_kazuki import get_prompt as get_nagisa_prompt
from chat.lilia_florence import get_parameters as get_lilia_parameters
from chat.lilia_florence import get_prompt as get_lilia_prompt
from dotenv import load_dotenv
from domain.model import AIMessage

load_dotenv()

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.7,
    max_tokens=None,
    request_timeout=None,
    max_retries=2
)



def chat_with_nagisa_kazuki(user_message):
    chain = get_nagisa_prompt() | llm.with_structured_output(AIMessage)
    parameters = get_nagisa_parameters(user_message)
    answer = chain.invoke(parameters)
    return answer

def chat_with_lilia_florence(user_message):
    chain = get_lilia_prompt() | llm.with_structured_output(AIMessage)
    parameters = get_lilia_parameters(user_message)
    answer = chain.invoke(parameters)
    return answer
