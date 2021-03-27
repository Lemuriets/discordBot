import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


GUILD_ID = 'guild id(here is my server token)'


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @cog_ext.cog_slash(name='help', guild_ids=[GUILD_ID])
    async def _help(self, ctx: SlashContext) -> None:
        with open('helpCommand.txt', 'r', encoding='utf-8') as helpFile:
            text = helpFile.read()

        emb = discord.Embed(title='Help', color=0xd90000)
        emb.add_field(name='Немного обо мне : ', value=text)
        emb.set_thumbnail(url=r'https://images-ext-2.discordapp.net/external/MpPbiOTbsu7q9mZuoHn3TXgUlJ_3UmojuxFh58LTg9g/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/775352879842197525/b3efc97c46c22b9d54fc536bc1b29484.webp?width=653&height=653')
            
        await ctx.send(embed=emb)

    @cog_ext.cog_slash(name='profile', guild_ids=[GUILD_ID])
    async def profile(self, ctx: SlashContext, member: discord.Member) -> None:
        # if member is None:
        #     member = ctx.author
        emb = discord.Embed(title=f'Информация о пользователе', color=0xd90000)
        emb.add_field(name='Никнейм : ', value=member.mention, inline=False)
        emb.add_field(name='id пользователя :', value=member.id)

        user_joined = str(member.joined_at)[:19]
        day = user_joined[8:10:]
        month = user_joined[5:7:]
        year = user_joined[0:4]
        
        emb.add_field(name='Присоединился : ', value=f'{day}.{month}.{year} {user_joined[11:19]}', inline=False)
        emb.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=emb)


    @cog_ext.cog_slash(name='avatar', guild_ids=[GUILD_ID])
    async def avatar(self, ctx: SlashContext, member: discord.Member) -> None:
        # if member is None:
        #     member = ctx.author
        emb = discord.Embed(title=f'Аватар {member.display_name}', color=0xd90000)
        emb.set_image(url=member.avatar_url)
        await ctx.send(embed=emb)


    @cog_ext.cog_slash(name='test', guild_ids=[GUILD_ID])
    @commands.has_permissions(administrator=True)
    async def test(self, ctx) -> None:
        emb = discord.Embed(title='Получение ролей', description='Выберите языки программирования, которые Вы учите', color=0xd00000)
        python = '<:python:813699136813400074> <@&818158742452437002>' # эмодзи, роль
        js = '<:javascript:777077082937229312> <@&818158742985375794>'
        cpp = '<:cpp:813699516804497408> <@&818158743619371008>'
        cs = '<:cs:813699658152280064> <@&818158744310382633>'
        c = '<:c_:813700485969870868> <@&818158747686797383>'
        html = '<:html:813700928631734273> <@&818161128509145158>'
        css = '<:css:813701153933492264> <@&818158745116606504>'
        php = '<:php:813701658164592670> <@&818158745673793578>'
        java = '<:java:813702088290598932> <@&818158746349600788>'

        emb.add_field(name='** **', value=f'{python}\n\n{cs}\n\n{css}')
        emb.add_field(name='** **', value=f'{js}\n\n{c}\n\n{php}')
        emb.add_field(name='** **', value=f'{cpp}\n\n{html}\n\n{java}')
        await ctx.send(embed=emb)


    @cog_ext.cog_slash(name='kick', guild_ids=[GUILD_ID])
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx: SlashContext, member: discord.Member) -> None:
        # if member is None:
        #     await ctx.send(embed=discord.Embed(title='Не указан пользователь', color=0xd00000))
        #     return None
        kick_message = discord.Embed(title='Кик пользователя', description=f'Пользователь {member.mention} был кикнут', color=0xd00000)
        await ctx.send(embed=kick_message)
        await member.kick()


    @cog_ext.cog_slash(name='ban', guild_ids=[GUILD_ID])
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx: SlashContext, member: discord.Member) -> None:
        # if member is None:
        #     await ctx.send(embed=discord.Embed(title='Не указан пользователь', color=0xd00000))
        #     return None
        ban_message = discord.Embed(title='Бан пользователя', description=f'Пользователь {member.mention} был забанен', color=0xd00000)
        await ctx.send(embed=ban_message)
        await member.ban()


    @cog_ext.cog_slash(name='fullmute', guild_ids=[GUILD_ID])
    @commands.has_permissions(administrator=True)
    async def fullmute(self, ctx: SlashContext, member: discord.Member) -> None:
        # if member is None:
        #     await ctx.send(embed=discord.Embed(title='пользователь не указан', color=0xd00000))
        #     return None
        guild = self.bot.get_guild(GUILD_ID)
        fullMuteRole = guild.get_role(818171126492299266)

        await member.add_roles(fullMuteRole)
        muteMessage = discord.Embed(title='Мут пользователя', description=f'Пользователь {member.mention} был замьючен', color=0xd00000)

        await ctx.send(embed=muteMessage)


    @cog_ext.cog_slash(name='unmute', guild_ids=[GUILD_ID])
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx: SlashContext, member: discord.Member) -> None:
        if member is None:
            await ctx.send(embed=discord.Embed(title='Не указан пользователь', color=0xd00000))
            return None 
        guild = self.bot.get_guild(GUILD_ID)
        unmute_role = guild.get_role(818171126492299266)
        await member.remove_roles(unmute_role)
        unmuteMessage = discord.Embed(title='Разут пользователя', description=f'Пользователь {member.mention} был размьючен', color=0x15ff00)
        await ctx.send(embed=unmuteMessage)


    @cog_ext.cog_slash(name='clear', guild_ids=[GUILD_ID])
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx: SlashContext, value: int) -> None:
        if value >= 50:
            await ctx.send(embed=discord.Embed(title='указанно слишком много сообщений', color=0xd00000))
            return None
        await ctx.channel.purge(limit=value + 1)
