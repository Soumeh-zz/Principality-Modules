from discord.ext import commands
from discord import Embed
from random import choice
from utils import not_self, error_message, module_help
from debug_utils import print_exception

class Roll(commands.Cog):
    def help_message(self):
        return """Roll a questionably large die.
`{0} (number) [multiplier]`
\> Roll a (number) sided die.
  Optionally, roll [multiplier] more die.""".format(self.prefix + 'roll')
    @commands.command()
    @not_self()
    async def roll(self, ctx):
        args = ctx.message.content.split()[1:]
        if not args:
            return await module_help(ctx.channel, self)
        if args[0] == 'e':
            return await ctx.channel.send('inva:fire: argment')
        try:
            if len(args) == 1:
                msg = await self.one_roll(args[0])
            elif len(args) == 2:
                msg = await self.mult_rolls(args[0], args[1])
            else:
                return await error_message(ctx.channel, "Too many arguments")
        except self.InvalidArgs as reason:
            return await error_message(ctx, reason)
        except Exception:
            return await error_message(ctx, "Argument must be a whole number larger than 1")
        await ctx.channel.send(embed=Embed(description=ctx.author.mention + ' ' + msg))
    class InvalidArgs(Exception):
        pass
    async def one_roll(self, number):
        number = int(number)
        if number == 1:
            raise self.InvalidArgs("Argument must be a whole number larger than 1")
        if number > 1000:
            raise self.InvalidArgs("Number can't be larger than 1000")
        random_number = self.random_number(number)
        return "rolled a D{0}, and it landed on **{1}**!".format(number, random_number)
    async def mult_rolls(self, number, mult):
        number, mult = int(number), int(mult)
        if number == 1 or mult == 1:
            raise self.InvalidArgs("Argument must be a whole number larger than 1")
        if number > 1000:
            raise self.InvalidArgs("Number can't be larger than 1000")
        if number > 30:
            raise self.InvalidArgs("Amount can't be larger than 30")
        random_numbers = []
        for i in range(mult):
            random_numbers.append(self.random_number(number))
        return "rolled {0}D{1}, and they landed on {2}! [{3}]".format(mult, number, ' and'.join(', '.join(['**' + str(n) + '**' for n in random_numbers]).rsplit(',', 1)), sum(random_numbers))
    def random_number(self, num):
        return choice(range(1, num + 1))