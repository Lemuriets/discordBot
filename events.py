import discord
from discord.ext import commands
import json


GUILD_ID = 'guild id(here is my server token)'


with open('roles.json', 'r', encoding='utf-8') as rfile:
    ROLES = json.load(rfile)['roles']


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print('Bot is running')
        game = discord.Game(name='-help')
        await self.bot.change_presence(status='online', activity=game)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != 818561931652497459:
            return None

        await message.add_reaction('✅')
        await message.add_reaction('⛔')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error) -> None:
        if isinstance(error,  discord.ext.commands.errors.CommandNotFound):
            await ctx.send('такой команды не существует')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload) -> None:
        if payload.message_id != 818167714954477601: # id сообщения
            return None
        member = payload.member
        guild = self.bot.get_guild(payload.guild_id)
        log_channel = self.bot.get_channel(814798560532103216) # получение канала для логов

        if payload.emoji.name not in ROLES:
            log = discord.Embed(title='Ошибка', description='Ошибка при выдаче роли', color=0xd00000)
            await log_channel.send(embed=log)
            return None

        role = guild.get_role(ROLES[payload.emoji.name])
        await member.add_roles(role)

        log = discord.Embed(title='Получение роли',
                            description=f'Пользователь {payload.member.mention} получил роль {role.mention}',
                            color=0x15ff00)
        await log_channel.send(embed=log)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload) -> None:
        if payload.message_id != 818167714954477601: # id сообщения
            return None
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        log_channel = self.bot.get_channel(814798560532103216) # получение канала для логов

        if payload.emoji.name not in ROLES:
            log = discord.Embed(title='Ошибка', description='Ошибка при отказе от роли', color=0xd00000)
            await log_channel.send(embed=log)
            return None

        role = guild.get_role(ROLES[payload.emoji.name])
        await member.remove_roles(role)

        log = discord.Embed(title='Отказ от роли роли',
                            description=f'Пользователь {member.mention} отказался от роли {role.mention}',
                            color=0xd00000)
        await log_channel.send(embed=log)

    @commands.Cog.listener()
    async def on_member_join(self, member) -> None:
        channel = self.bot.get_channel(773428781058359318)
        emb = discord.Embed(title='Приветствие', color=0xb000b1)
        emb.set_thumbnail(url=member.avatar_url)
        emb.add_field(name='** **', value=f'Пользователь {member.mention} зашел на наш сервер)')

        guild = self.bot.get_guild(GUILD_ID)
        hello_role = guild.get_role(818161833999335455)
        await member.add_roles(hello_role)
        await channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_member_remove(self, member) -> None:
        channel = self.bot.get_channel(775103622614614026)
        bye_message = discord.Embed(title='Покинул нас', color=0xd00000)
        bye_message.set_thumbnail(url=member.avatar_url)
        bye_message.add_field(name='** **', value=f'Пользователь {member.mention} покинул нас')
        await channel.send(embed=bye_message)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after) -> None:
        guild = self.bot.get_guild(GUILD_ID)
        category = discord.utils.get(guild.categories, id=819652663977181214)

        if after.channel is not None:
            if after.channel.id == 818431570800934913:
                author = str(member)[:-5:]
                created_channel = await guild.create_voice_channel(name='『🎧』┃' + author, category=category)
                await member.move_to(created_channel)

                def check(*args):
                    return len(created_channel.members) == 0

                await self.bot.wait_for("voice_state_update", check=check)
                await created_channel.delete()