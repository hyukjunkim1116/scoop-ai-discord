from repository import UserRepository as userRepository
from repository import CharacterRepository as characterRepository
from repository import ChatRepository as chatRepository
class UserService:

    @staticmethod
    async def initialize_user(user_id: int):
        return userRepository().initialize_user(user_id)

    @staticmethod
    async def delete_user(member,discord):
        member_id = member.id
        userRepository().delete_user(member_id)
        characterRepository().delete_all(member_id)
        chatRepository().delete_all(member_id)
        characters = characterRepository().get_characters_by_user_id(member_id)
        for character in characters:
            channel_id = character.get('channel_id')
            print(channel_id,"channel_id")
            channel = member.guild.get_channel(int(channel_id))
            role = discord.utils.get(member.guild.roles, name=str(channel_id))
            if role is not None:
                await role.delete(reason=f"User {member_id} was removed")
            if channel is not None:
                await channel.delete(reason=f"User {member_id} was removed")


    @staticmethod
    async def send_welcome_message(member):
        print(f"ID: {member.id}")
        guild = member.guild
        main_channel_id = 1344347307151196262
        main_channel = guild.get_channel(main_channel_id)

        welcome_message = (
                f"안녕하세요, {member.mention}님! Scoop 서버에 오신 것을 환영합니다! 🎉\n"
                f"**`!캐릭터생성 [캐릭터 이름]`** - 새로운 캐릭터와 전용 채널을 생성해주세요!.\n"
                f"**`채널을 나갈 경우 모든 채팅과 캐릭터는 삭제됩니다.`**\n"
            )
        await main_channel.send(welcome_message)