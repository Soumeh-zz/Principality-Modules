from discord.ext import commands
from utils import not_self
from random import choice

class Greeting(commands.Cog):
    greetings = ['hello', 'sup', 'hi', 'yo', 'hey']
    def help_message(self):
        return 'Replies whenever someone greets SorrowBot.'
    @commands.Cog.listener()
    async def on_message(self, message):
        bot = message.guild.me
        cont = message.content.lower()
        if bot.display_name.lower() in cont or bot.name.lower() in cont:
            for greet in self.greetings:
                bot = message.guild.me
                if greet + ' ' + bot.name.lower() in cont or greet + ' ' + bot.display_name.lower() in cont:
                    return await message.channel.send(choice(self.greetings).title() + ' ' + message.author.name + '!')