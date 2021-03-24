from discord.ext import commands
from utils import not_self, embed_message

class Suggestions(commands.Cog):
    def __init__(self):
        self.suggestions_channel = 807271131924660264
        self.suggestion_discussion_channel = 630500899654991888
    async def __asinit__(self):
        self.suggestion_discussion_channel = await self.bot.fetch_channel(self.suggestion_discussion_channel)
        channel = await self.bot.fetch_channel(self.suggestions_channel)
        bot_user = self.bot.user
        messages = []
        async for message in channel.history(limit=100):
            if not message.reactions:
                messages.append(message)
                continue
            users = sum([await reaction.users().flatten() for reaction in message.reactions], [])
            if bot_user in users:
                break
            else:
                messages.append(message)
        for message in reversed(messages):
            await self.suggest(message)
    def help_message(self):
        return "Tracks suggestions posted in <#{0}> and posts them in <#{1}>".format(self.suggestions_channel, self.suggestion_discussion_channel.id)
    @commands.Cog.listener()
    @not_self()
    async def on_message(self, message):
        if message.channel.id == self.suggestions_channel:
            if str(message.type) == 'MessageType.pins_add':
                return
            await self.suggest(message)
    async def suggest(self, message):
        for emoji in ['✅', ':white_x_mark:737044020165083289']:
            await message.add_reaction(emoji)
        await embed_message(self.suggestion_discussion_channel, message)