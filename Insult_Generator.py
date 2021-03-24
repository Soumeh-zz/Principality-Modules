from discord.ext import commands
from utils import not_self, generate_insult

class Insult_Generator(commands.Cog):
    def help_message(self):
        return """Generate random insults.
``{0}``
 \> Returns a procedurally generated insult.
``{0} s``
 \> Returns a procedurally generated PG-13 insult.""".format(self.prefix + 'insult')
    @commands.command()
    @not_self()
    async def insult(self, ctx):
        try:
            sub = ctx.message.content.split()[1]
            if sub == 's':
                insult = generate_insult(True)
            else:
                raise IndexError
        except IndexError:
            insult = generate_insult()
        await ctx.channel.send(insult)