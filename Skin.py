from discord.ext import commands
from discord import Embed, File
from utils import not_self, error_message, module_help, get_JSON, url_to_file
from base64 import b64decode
from io import BytesIO
from PIL import Image
from json import loads

class Skin(commands.Cog):
    def help_message(self):
        return """Send a player's Minecraft skin.
``{0} <player>``
\> Returns a Minecraft player's skin.""".format(self.prefix + 'skin')
    @commands.command()
    @not_self()
    async def skin(self, ctx):
        try:
            skin_name = ctx.message.content.split()[1]
        except IndexError:
            return await module_help(ctx.channel, self)
        images = []
        json1 = await get_JSON('https://api.mojang.com/users/profiles/minecraft/' + skin_name)
        if not json1:
            return await error_message(ctx.channel, "Unknown player")
        skin_name = json1['name']
        json2 = await get_JSON('https://sessionserver.mojang.com/session/minecraft/profile/' + json1['id'])
        data = json2['properties'][0]['value']
        data = b64decode(data).decode('utf-8')

        skin_link = loads(data)['textures']['SKIN']['url']
        image = await url_to_file(skin_link)
        skin_image = Image.open(image)
        size = skin_image.size
        skin_image = skin_image.resize((size[0] * 8, size[1] * 8), Image.NEAREST)
        image = BytesIO()
        skin_image.save(image, 'png')
        image.seek(0)

        file = File(image, filename=skin_name + '_large.png')
        if not skin_name.lower().endswith('s'):
            desc = "**{}**'s Skin:".format(skin_name)
        else:
            desc = "**{}**' Skin:".format(skin_name)
        embed = Embed(description=desc)
        embed.set_thumbnail(url=skin_link)
        embed.set_image(url='attachment://' + file.filename)
        await ctx.channel.send(file=file, embed=embed)