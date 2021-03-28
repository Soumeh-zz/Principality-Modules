from discord import NotFound
from discord.ext import commands
from utils import not_self, embed_message
from start import prefix

class Embed_Links(commands.Cog):
    def help_message(self):
        return """Sends an embed displaying the content of linked messages.
Turn on developer mode to copy message links."""
    @commands.Cog.listener()
    @not_self()
    async def on_message(self, message):
        args = message.content.lower()
        if 'https://' in args and 'discord' in args:
            for word in args.split():
                if 'https://' not in word:
                    continue
                domain = word.split('https://', 1)[1].split('.com/channels/', 1)[0]
                if 'discord' in domain and 'cdn' not in domain:
                    try:
                        linked_message = await self.link_to_message(word)
                    except:
                        linked_message = None
                    if linked_message:
                        await embed_message(message.channel, linked_message)
    async def link_to_message(self, link):
        try:
            data = link.split('/channels/')[1].split('/')
        except IndexError:
            return None
        linked_channel = await self.bot.fetch_channel(int(data[1]))
        return await linked_channel.fetch_message(int(data[2]))