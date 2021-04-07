from discord import NotFound, MessageType
from discord.errors import HTTPException
from discord.ext import commands
from utils import not_self, get_config, embed_message, ChannelNotFound
import inspect

class Suggestions(commands.Cog):
    def __init__(self):
        default_config = """
channel = 1234567891234567891 # what channel should suggestions get sent in?
discussion_channel = 1234567891234567891 # what channel should suggestion discussions be in?
yes_emoji = "✅" # if you are using a custom emoji, make sure to add the emoji's ID to the string and surrond it with <>, e.g. '<:emoji:123412341234>'
no_emoji = "❌"
        """
        self.config = get_config(self, default_config)
    async def __asinit__(self):
        try:
            self.suggestion_discussion_channel = await self.bot.fetch_channel(self.config['discussion_channel'])
        except NotFound:
            raise ChannelNotFound(self.config['discussion_channel'])
        try:
            channel = await self.bot.fetch_channel(self.config['channel'])
        except NotFound:
            raise ChannelNotFound(self.config['channel'])
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
        return "Tracks suggestions posted in <#{0}> and posts them in <#{1}>".format(self.config['channel'], self.suggestion_discussion_channel.id)
    @commands.Cog.listener()
    @not_self()
    async def on_message(self, message):
        if message.channel.id == self.config['channel']:
            await self.suggest(message)
    async def suggest(self, message):
        if message.author == self.bot.user or message.type != MessageType.default:
            return
        for emoji in [self.config['yes_emoji'], self.config['no_emoji']]:
            try:
                await message.add_reaction(emoji)
            except HTTPException:
                print("Unknown emoji '{}'".format(emoji))
        await embed_message(self.suggestion_discussion_channel, message)