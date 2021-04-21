from discord.ext import commands
from utils import not_self

class Poll(commands.Cog):
    command = ['(S)', 'Poll;']
    def help_message(self):
        return 'Reacts with [✅] and [X] emotes on messages starting with "{0[0]}" or "{0[1]}"...'.format(self.command)
    @commands.Cog.listener()
    @not_self()
    async def on_message(self, message):
        for command in self.command:
            if message.content.lower().startswith(command.lower()):
                for emoji in ['✅', ':white_x_mark:737044020165083289']:
                    await message.add_reaction(emoji)

class Yes_Poll(commands.Cog):
    command = ['{S}', 'Poll..']
    def help_message(self):
        return 'Reacts with 2 (two) [✅] emotes on messages starting with "{0[0]}" or "{0[1]}".'.format(self.command)
    @commands.Cog.listener()
    @not_self()
    async def on_message(self, message):
        for command in self.command:
            if message.content.lower().startswith(command.lower()):
                for emoji in ['✅', ':whiter_checker_marker:752987624188280972']:
                    await message.add_reaction(emoji)