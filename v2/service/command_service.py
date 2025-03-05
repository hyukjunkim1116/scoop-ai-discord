from v2.repository import ChannelRepository as channelRepository
from v2.repository import Prompt
async def send_welcome_message(member):
        main_channel_id = 1346305231440318555
        guild = member.guild

        main_channel = guild.get_channel(main_channel_id)

        welcome_message = (
            f"안녕하세요, {member.mention}님! 스쿠핑 서버에 오신 것을 환영합니다! 🎉\n\n"
            f"**!캐릭터 명령어로 캐릭터의 정보를 확인할 수 있습니다.**\n\n"
            f"**채팅방은 두 가지 유형이 있습니다:**\n\n"
            f"• **프라이빗 채팅방**: 1:1 대화로 다른 사용자에게 보이지 않습니다.\n\n"
            f"• !비밀챗 [캐릭터 이름]으로 캐릭터와 1:1 대화를 시작해보세요!\n\n"
            f"• **오픈 채팅방**: 모든 사용자가 참여하고 볼 수 있는 공개 채팅방입니다.\n\n"
            f"**`채널을 나갈 경우 모든 채팅과 캐릭터는 삭제됩니다.`**"
        )
        await main_channel.send(welcome_message)

async def create_private_channel(ctx,character_name: str):
    if character_name not in Prompt.CHARACTER_PRIVATE_MAP.value:
        return await ctx.send("존재하지 않는 캐릭터입니다.")
    if character_name == "":
        return await ctx.send("캐릭터 이름을 입력해주세요. 예시: !비밀챗 <캐릭터이름>")
    guild = ctx.guild
    user = ctx.author

    channel = await guild.create_text_channel(name=f"🔞비밀채팅방-{character_name}")
    print("channel created",channel)
    await channel.edit(nsfw=True)
    webhook = await channel.create_webhook(name=channel.id)
    await channel.set_permissions(guild.default_role, read_messages=False)
    await channel.set_permissions(user, read_messages=True, send_messages=True)

    channelRepository().create_channel(character_name, user.id, channel.id, webhook.url)
    await ctx.send(f"{channel.mention}에서 `{character_name}`와 대화를 시작하세요!")
    await channel.send(f"🔞비밀 채팅을 시작해보세요!")

async def create_public_channel(ctx, character_name: str):
    guild = ctx.guild
    user = ctx.author
    channel = await guild.create_text_channel(name=f"🌿-{character_name}🍦")
    webhook = await channel.create_webhook(name=channel.id)
    is_private = False
    channelRepository().create_channel(character_name, user.id, channel.id, webhook.url,is_private)



async def show_characters(ctx):
    character_message = (
        f"```ini\n[Scoop AI 캐릭터 라인업]```\n"
        f" **킹콩** - 야생의 본능을 간직한 독립적인 턱시도 고양이\n"
        f"**다미** - 항상 긍정적인 에너지를 전파하는 친절한 친구\n\n"
        f"**큐티예나** - 10마리 강아지와 사는 사랑스러운 소녀\n\n"
        f"**흑진** - 마음을 쉽게 열지 않는 신비로운 미소년\n\n"
        f"**보이드 레조넌스** - 시간과 공간을 초월한 혼돈의 존재\n\n"
        f"-----------------------------------------------\n\n"
        f"**🔞제이슨** - 모델 출신의 매력적인 바텐더\n\n"
        f"**🔞셀레나** - 매혹적인 외모와 지적인 대화 능력을 겸비한 클럽 댄서\n\n"
        f"⭐ **지금 바로 AI 캐릭터와 대화를 시작해보세요!** ⭐\n\n"
        f"명령어: `!비밀챗 [🔞캐릭터 중 하나의 이름]`"
    )
    return await ctx.send(character_message)