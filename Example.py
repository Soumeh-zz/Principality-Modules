# general notice, only put one class inside of a module, else shit might break

# classes that are generated before runtime:
# self.bot = the bot object
# self.prefix = the prefix in the config file

from discord.ext import commands # important, do not remove
#from utils import not_self

class Example(commands.Cog): # only edit the classname here
    #def __init__(self):
    #   pass

    def help_message(self): # used for the /help command
        return "Example help message" # just return any string, look at how the other help messages are formatted

    ##@commands.command()
    ##@not_self() # only listens if the message wasn't sent by the bot
    ##async def command_name(self, ctx):
    # ctx.message to get the message object
    # 

    ##@commands.Cog.listen()
    ##async def event_name(self, args):
    # for a list of events, go to https://discordpy.readthedocs.io/en/latest/api.html#event-reference
    # arguments are different depending on the event