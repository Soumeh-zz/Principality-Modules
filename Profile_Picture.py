from discord.ext import commands
from discord import File, Embed
from utils import not_self, error_message

class Profile_Picture(commands.Cog):
    def help_message(self):
        return """Get someone's profile picture.
`{0} (name)`
\> Posts a server member's profile picture.""".format(self.prefix + 'pfp')
    @commands.command()
    @not_self()
    async def pfp(self, ctx):
        try:
            arguments = ctx.message.content.split(' ', 1)[1]
            member = ctx.guild.get_member_named(arguments)
        except IndexError:
            member = ctx.author
        if not member:
            return await error_message(ctx.channel, "Unknown member")
        embed = Embed(description="<@{}>'s Profile Picture:".format(member.id))
        embed.set_image(url=member.avatar_url)
        await ctx.channel.send(embed=embed)