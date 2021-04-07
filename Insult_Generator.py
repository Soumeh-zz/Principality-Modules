from discord.ext import commands
from utils import not_self

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
                insult = self.generate_insult(True)
            else:
                raise IndexError
        except IndexError:
            insult = self.generate_insult()
        await ctx.channel.send(insult)
    def generate_insult(safe=False):
        main = ['well played (noun)', 'you are (adjct) (noun)', 'you are (adjct) (noun)', 'eat a (noun) (noun)',
        'eat a (noun)', '(verb)', 'i will (verb) you', 'who is this (adjct) (noun)']
        insults = {
        "noun": ['nerd', 'weakling', 'dork', 'donkey', 'maggot', 'cretin', 'jerk', 'idiot', 'fool', 'butt', 'nerd', 'freak', 'buffoon', 'tool',
        'dunce', 'blockhead', 'pinhead', 'chump', 'donkey', 'muppet'],
        "verb": ['kiss', 'kick', 'punch'],
        "adjct": ['french', 'stupid', 'weak', 'dumb', 'fat', 'ugly', 'thick', 'daft', 'long', 'tiny', 'bumbling', 'absolute']
        }
        if not safe:
            main += ['i will (verb) your mother', '(verb) yourself', '(verb) you', 'i (verb) in your room', 'choke on a (noun) and (verb)']
            newInsults = {
            "noun": ['retard', 'fuck', 'shit', 'ass', 'imbecile', 'ass', 'asshole', 'turd', 'sucker', 'piss', 'bitch', 'tard', 'fuckhead'],
            "verb": ['fuck', 'shit', 'kill', 'shit', 'hang', 'pass'],
            "adjct": ['retarded', 'motherfucking']
            }
            for key, values in newInsults.items():
                for value in values:
                    insults[key].append(value)
        insult = choice(main)
        for key, key_insults in insults.items():
            key = '(' + key + ')'
            while key in insult:
                insult = insult.replace(key, choice(key_insults), 1)
        remove_characters = choice(range(-2, 3))
        while remove_characters > 0:
            insult = insult.replace(insult[choice(range(len(insult)))], '', 1)
            remove_characters -= 1
        return insult