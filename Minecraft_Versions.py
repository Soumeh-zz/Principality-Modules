from discord.ext import commands
from discord import Embed
from aiohttp import ClientSession
from json import loads
from lxml import html
from utils import not_self, error_message

from debug_utils import print_exception

class Minecraft_Versions(commands.Cog):
    def help_message(self):
        return """Get information about Minecraft's latest releases.
`{0}`
\> Sends info from the wiki page of the latest version of Minecraft.
`{0} (version)`
\> Sends info from the wiki page of a (specified version) of Minecraft.""".format(self.prefix + 'mcversion')
    @commands.command()
    @not_self()
    async def mcversion(self, ctx):
        try:
            try:
                args = ctx.message.content.split(' ', 1)[1]
                sub = args.split()[0].lower()
                if sub == 'latest':
                    await self.post_version(ctx.channel)
                else:
                    await self.post_version(ctx.channel, args)
            except IndexError:
                await self.post_version(ctx.channel)
        except Exception as e:
            print_exception(e)
    async def post_version(self, channel, version=None):
        link = await self.generate_link(version)
        tree = await self.link_to_html(link)
        if not len(tree):
            return await error_message(channel, "Invalid version")
        image_link = 'https://minecraft.gamepedia.com' + tree.xpath('//div[@class="infobox-imagearea animated-container"]/div/a/@href')[0]
        img_tree = await self.link_to_html(image_link)
        image = img_tree.xpath('//div[@class="fullImageLink"]/a/@href')[0]
        title = link.split('https://minecraft.gamepedia.com/')[1].replace('_', ' ')
        features_map = {}
        path = '//div[@class="mw-parser-output"]/'
        i = 1
        while len(str(features_map)) < 512:
            key = tree.xpath(path + 'dl[{0}]/dt/descendant-or-self::*/text()'.format(i))[0]
            value = ['• ' + ''.join(i.xpath('descendant-or-self::*/text()')) for i in tree.xpath(path + 'ul[{}]/li'.format(i))]
            features_map[key] = value
            i += 1
        while len(str(features_map)) > 1536:
            del features_map[features_map.keys()[-1]][-1]
        if '-pre' in title:
            title = title.replace('-pre', ' Pre-release ')
        embed = Embed(description="**[{0}]({1})**".format(title, link))
        embed.set_image(url=image)
        for key, value in features_map.items():
            if not key:
                key = '\u200b'
            if not value:
                value = '\u200b'
            embed.add_field(name=key, value='\n'.join(value), inline=False)
        await channel.send(embed=embed)
    async def link_to_html(self, link):
        async with ClientSession() as session:
            async with session.get(link) as resp:
                if resp.status == 404:
                    return []
                return html.fromstring(await resp.text())
    async def generate_link(self, version=None):
        if version:
            link = 'https://minecraft.gamepedia.com/Java_Edition_' + version.lower()
        else:
            async with ClientSession() as session:
                async with session.get('https://launchermeta.mojang.com/mc/game/version_manifest.json') as resp:
                    json = await resp.text()
                    latest = loads(json)['versions'][0]
            link = 'https://minecraft.gamepedia.com/Java_Edition_' + latest['id']
        return link