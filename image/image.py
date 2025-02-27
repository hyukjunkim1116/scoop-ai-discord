from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


class ImageGenerator:
    def __init__(self):
        # 환경 변수 로드
        load_dotenv()
        self.dalle = DallEAPIWrapper(
            model="dall-e-3"
        )
        self.chat = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.1)
        # 프롬프트 개선을 위한 체인 구성
        system_template = """당신은 DALL-E 이미지 생성을 위한 프롬프트 전문가입니다.
    사용자의 간단한 요청을 받아 DALL-E가 더 좋은 결과를 생성할 수 있도록 
    상세하고 명확한 프롬프트로 변환해주세요. 색상, 구도, 스타일, 분위기 등을 포함하세요.

    중요: 설명이나 소개 없이 개선된 프롬프트 텍스트만 정확히 반환하세요. 
    따옴표나 추가 텍스트 없이 개선된 프롬프트만 출력하세요."""

        human_template = "이 프롬프트를 개선해주세요: {original_prompt}"
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("human", human_template),
        ])

        self.prompt_chain = chat_prompt | self.chat | StrOutputParser()

    def improve_prompt(self, original_prompt):
        """LangChain의 체인을 사용하여 프롬프트 개선"""
        enhanced_prompt = self.prompt_chain.invoke({"original_prompt": original_prompt})
        return enhanced_prompt.strip()

    def generate_image(self, prompt, improve=True):
        """이미지 생성 및 URL 반환"""
        try:
            # 프롬프트 개선 옵션
            if improve:
                enhanced_prompt = self.improve_prompt(prompt)
                print(f"개선된 프롬프트: {enhanced_prompt}")
                final_prompt = enhanced_prompt
            else:
                final_prompt = prompt

            # DALL-E 3로 이미지 생성
            response = self.dalle.run(final_prompt)

            # 응답 파싱 (URL 추출)
            if isinstance(response, str):
                return response  # 이미 URL만 반환되는 경우
            elif isinstance(response, dict) and "url" in response:
                return response["url"]  # URL 키가 있는 경우
            else:
                return str(response)  # 기타 응답 형식

        except Exception as e:
            print(f"이미지 생성 중 오류 발생: {str(e)}")
            return None