from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()
llm = ChatOpenAI(model_name="gpt-4o-mini")

prompt = ChatPromptTemplate.from_template("You are an expert in astronomy. Answer the question. <Question>: {input}")
output_parser = StrOutputParser()

chain = prompt | llm | output_parser


def test():
    return chain.invoke({"input": "지구의 자전 주기는?"})


