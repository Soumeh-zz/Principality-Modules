from discord.ext import commands
from start import prefix
from utils import not_self, module_help, error_message, random_message, embed_message

class Random_Message(commands.Cog):
    def help_message(self):
        return """Returns a random message from a channel.
`{0} (channel)`
\> Sends an embed displaing a random message from the specified (channel).""".format(prefix + 'randmsg')
    @commands.command()
    @not_self()
    async def randmsg(self, ctx):
        try:
            arguments = ctx.message.content.split(' ', 1)[1]
        except IndexError:
            return await module_help(ctx.message.channel, self)
        try:
            channel_id = int(arguments.split('<#')[1].split('>')[0])
            channel = await self.bot.fetch_channel(channel_id)
        except:
            return await error_message(ctx.channel, "Unknown channel")
        if channel.is_nsfw() and not message.channel.is_nsfw():
            return await error_message(ctx.channel, "Messages from NSFW channels are exclusive")
        rand_message = await random_message(channel)
        await embed_message(ctx.channel, rand_message)