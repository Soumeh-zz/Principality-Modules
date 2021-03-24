from discord.ext import commands
from discord import Embed, File
from utils import not_self, url_to_file, error_message, module_help
from io import BytesIO
from PIL import Image
from math import ceil

class Pixel(commands.Cog):
    def help_message(self):
        return """Random utilities for pixel art.
`{0} upscale`
\> Upscales an attached image by 8.
`{0} tile`
\> Upscales an image by 4 and tiles in 3 times.""".format(self.prefix + 'pixel')
    @commands.command()
    @not_self()
    async def pixel(self, ctx):
        try:
            attachment = ctx.message.attachments[0]
            if attachment.filename.rsplit('.')[1] not in ['png', 'jpg', 'jpeg']:
                raise IndexError
            file = await url_to_file(attachment.proxy_url)
            image = Image.open(file)
        except IndexError:
            return await error_message(ctx.channel, "You must attach an image with this command")
        try:
            args = ctx.message.content.split(' ', 1)[1].split()
            sub = args[0].lower()
            if sub == 'tile':
                file = await self.tile(image)
            if sub == 'up' or sub == 'upscale':
                file = await self.up(image)
            if sub == 'info':
                return await self.info(ctx.channel, image, attachment.filename)
            return await self.post_file(ctx.channel, file, attachment)
        except IndexError:
            await module_help(ctx.channel, self)
    async def up(self, image):
        upscale = ceil(128 / max(image.size))
        image = image.resize((image.width * upscale, image.height * upscale), Image.NEAREST)
        file = BytesIO()
        image.save(file, 'png')
        file.seek(0)
        return file
    async def tile(self, image):
        upscale = ceil(64 / max(image.size))
        tiles = 3
        image = image.resize((image.width * upscale, image.height * upscale), Image.NEAREST)
        new_image = Image.new('RGBA', (image.width * tiles, image.height * tiles), (255, 0, 0, 0))
        for h in [i * image.height for i in range(tiles)]:
            for w in [i * image.height for i in range(tiles)]:
                new_image.paste(image, (h, w))
        file = BytesIO()
        new_image.save(file, 'png')
        file.seek(0)
        return file
    async def info(self, channel, image, filename):
        res = image.size
        upscale = ceil(128 / max(res))
        image = image.resize((image.width * upscale, image.height * upscale), Image.NEAREST)
        desc = "Resolution: **{}**".format('x'.join([str(i) for i in res]))
        desc += '\n' + "Total Color Count: **{}**".format(len(image.getcolors()))
        embed = Embed(title="Information:", description=desc)
        file = BytesIO()
        image.save(file, 'png')
        file.seek(0)
        file = File(file, filename=filename)
        embed.set_thumbnail(url='attachment://' + filename)
        return await channel.send(file=file, embed=embed)
    async def post_file(self, ctx, file, attachment):
        discord_file = File(file, filename=attachment.filename)
        desc = 'Original:' + ('\n``{}`` '.format(attachment.filename) if attachment.filename != 'unknown.png' else '')
        embed = Embed(description=desc)
        embed.set_thumbnail(url=attachment.proxy_url)
        embed.set_image(url='attachment://' + attachment.filename)
        await ctx.send(file=discord_file, embed=embed)