from discord.ext import commands
from discord import Embed, errors
from utils import not_self, int_to_ronum, int_to_full_ronum, error_message, module_help

class Number_To_RoNum(commands.Cog):
    def help_message(self):
        return """Converts a number to a roman numeral.
``{} (number)``
 \> Returns the Roman Numeral equivalent of a whole number.
   (Note: Try not to input numbers larger than 9999.)""".format(self.prefix + 'ronum')
    @commands.command()
    @not_self()
    async def ronum(self, ctx):
        args = ctx.message.content.split(' ', 1)[1].split()
        if not args:
            return await module_help(ctx.channel, self)
        try:
            try:
                arg = args[1].lower()
            except IndexError:
                arg = ''
            if arg == 'flat':
                await ctx.channel.send(int_to_full_ronum(int(args[0])))
            else:
                ronum = int_to_ronum(int(args[0]))
                desc = '{0} =\n{1}'.format(args[0], ronum)
                embed = Embed(description=desc)
                await ctx.channel.send(embed=embed)
        except errors.HTTPException:
            await error_message(ctx.channel, "Output is too long for Discord.")
        except ValueError:
            await error_message(ctx.channel, "Input must be a whole number.")