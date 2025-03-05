import discord
from v1.repository import CharacterRepository as characterRepository
class EmbedService:
    def __init__(self):
        self.discord = discord
    def get_chat_embed(self,situation, chat, affection):
        try:
            affection_value = int(affection)
            # 호감도에 따른 색상 (낮음: 회색, 중간: 푸른색, 높음: 분홍색)
            if affection_value < 30:
                color = 0x9e9e9e  # 회색
                heart_emoji = "💔"
            elif affection_value < 50:
                color = 0x64b5f6  # 연한 푸른색
                heart_emoji = "💙"
            elif affection_value < 70:
                color = 0x4caf50  # 녹색
                heart_emoji = "💚"
            elif affection_value < 85:
                color = 0xffa726  # 주황색
                heart_emoji = "🧡"
            else:
                color = 0xff4fa7  # 분홍색
                heart_emoji = "❤️"
        except ValueError:
            color = 0x00b0f4  # 기본 푸른색
            heart_emoji = "❓"

        # 상황을 기울임체로 만들기 (마크다운 사용)
        formatted_situation = f"*{situation}*"

        # 호감도 표시에 이모티콘 추가
        affection_display = f"{heart_emoji} **{affection}/100**"

        # 전체 내용을 하나의 description으로 구성
        full_description = f"{formatted_situation}\n\n{chat}\n\n{affection_display}"
        # 임베드 생성
        embed = self.discord.Embed(
            description=full_description,
            color=color
        )
        return embed


    def get_confirm_list(self,ctx):
        character = characterRepository().get_character_by_channel_id(ctx.channel.id)

        if not character:
            return

        # 속성 목록
        attributes = [
            ("이름", "character_name"),
            ("성별", "gender"),
            ("소개", "intro"),
            ("MBTI", "mbti"),
            ("초기 호감도", "init_affection"),
            ("세계관", "world_view"),
            ("초기 대화", "init_chat"),
            ("초기 상황", "init_situation"),
            ("비밀", "secret"),
        ]
        # 결과 메시지 생성
        embed = self.discord.Embed(
            title=f"'{character.get('character_name', '알 수 없음')}' 캐릭터 정보",
            description="캐릭터 설정 상태를 확인합니다.",
            color=0x3498db  # 파란색
        )

        for display_name, attr_name in attributes:
            # 속성값 가져오기, 없으면 "X"로 표시
            value = character.get(attr_name, "X")

            # 값이 너무 길면 일부만 표시
            if isinstance(value, str) and len(value) > 100:
                value = value[:97] + "..."

            # 비밀의 경우 실제 내용은 보여주지 않음
            if attr_name == "secret" and value != "X":
                value = "⭐ 설정됨"

            # 임베드에 필드 추가
            embed.add_field(
                name=f"📝 {display_name}",
                value=value,
                inline=False
            )

        # 설정 완료 여부 확인
        required_fields = ["gender", "intro", "mbti", "init_affection",
                           "world_view", "init_chat", "init_situation"]

        all_set = all(character.get(field) for field in required_fields)

        if all_set:
            embed.set_footer(text="모든 필수 설정이 완료되었습니다! '!시작' 명령어로 대화를 시작할 수 있습니다.")
            embed.color = 0x2ecc71  # 초록색
        else:
            missing = [attr for attr, field in [
                ("성별", "gender"),
                ("소개", "intro"),
                ("MBTI", "mbti"),
                ("초기 호감도", "init_affection"),
                ("세계관", "world_view"),
                ("초기 대화", "init_chat"),
                ("초기 상황", "init_situation"),
                ("비밀", "secret"),
            ] if not character.get(field)]

            embed.set_footer(text=f"아직 설정이 필요합니다: {', '.join(missing)}")
            embed.color = 0xe74c3c  # 빨간색
        return embed

    def get_help_embed(self):
        """봇 명령어 사용법을 보여줍니다."""

        embed = self.discord.Embed(
            title="🤖 Scoop AI 캐릭터 챗봇 사용 설명서",
            description="나만의 AI 캐릭터를 만들고 대화해보세요!",
            color=0x00b0f4  # 파란색 계열
        )

        # 캐릭터 생성 및 관리
        embed.add_field(
            name="🎭 캐릭터 생성 및 시작",
            value=(
                "**`!시작`** - 캐릭터와의 대화를 시작합니다. (모든 설정 완료 후)\n"
                "**`!확인`** - 현재 캐릭터의 설정 상태를 확인합니다."
            ),
            inline=False
        )

        # 캐릭터 설정
        embed.add_field(
            name="✏️ 캐릭터 설정하기",
            value=(
                "**`!성별 [내용]`** - 캐릭터의 성별을 설정합니다.\n"
                "**`!소개 [내용]`** - 캐릭터의 소개글을 설정합니다.\n"
                "**`!mbti [유형]`** - 캐릭터의 MBTI 성격 유형을 설정합니다.\n"
                "**`!시작호감도 [0~100]`** - 캐릭터의 초기 호감도를 설정합니다.\n"
                "**`!세계관 [내용]`** - 캐릭터가 속한 세계관을 설정합니다.\n"
                "**`!처음상황 [내용]`** - 대화가 시작되는 상황을 설정합니다.\n"
                "**`!첫메세지 [내용]`** - 캐릭터가 처음 보낼 메시지를 설정합니다.\n"
                "**`!비밀 [내용]`** - 캐릭터의 비밀이나 숨겨진 설정을 추가합니다.\n"
                "**`!이미지프롬프트 [내용]`** - 캐릭터 이미지 생성용 프롬프트를 설정합니다."
            ),
            inline=False
        )

        # 사용 예시
        embed.add_field(
            name="📝 사용 예시",
            value=(
                "1. **`!캐릭터생성 나기사`** - '나기사'라는 이름의 캐릭터 생성\n"
                "2. **`!성별 여성`**, **`!mbti ENFP`** 등으로 캐릭터 속성 설정\n"
                "3. **`!확인`** - 모든 필요한 설정이 완료되었는지 확인\n"
                "4. **`!시작`** - 캐릭터와 대화 시작\n"
                "5. 이제 채널에 일반 메시지를 입력하면 캐릭터와 대화할 수 있습니다!"
            ),
            inline=False
        )

        # 팁
        embed.add_field(
            name="💡 팁",
            value=(
                "• 모든 설정은 캐릭터의 채널에서 입력해야 합니다.\n"
                "• 캐릭터 설정이 많을수록 더 개성있는 대화가 가능합니다.\n"
                "• 세계관과 상황 설정을 자세히 적으면 캐릭터의 대답이 더 풍부해집니다."
            ),
            inline=False
        )

        embed.set_footer(text="Powered by Scoop AI | 추가 도움이 필요하면 관리자에게 문의하세요.")
        return embed
