from discord import Embed
from discord.ext import commands
from utils import get_embed_from_json, not_self, error_message, module_help
from json import loads, JSONDecodeError
from aiohttp import ClientSession, InvalidURL
from debug_utils import print_exception

class Custom_Embeds(commands.Cog):
    def help_message(self):
        return """Admin only! Send embed messages from JSON strings.
`{0} link (url)`
\> Embed from an URL that links to raw JSON string.
`{0} file (file)`
\> Eembed from a .json file inside of 'modules/embeds'.
`{0} (json)`
\> Embed from the input as a JSON string.""".format(self.prefix + 'embed')
    @commands.command()
    @not_self()
    async def embed(self, ctx):
        if not ctx.channel.permissions_for(ctx.author).administrator and not ctx.author.id == 277796269907378176:
            return await error_message(ctx.channel, "You need to be an administrator to use this command.")
        try:
            args = ctx.message.content.split(' ', 1)[1]
        except IndexError:
            return await module_help(ctx.channel, self)
        sub = args.split()[0]
        if sub.startswith('!'):
            sub = sub.split('!', 1)[1]
            await ctx.message.delete()
        if sub == 'link':
            try:
                url = args.split(' ', 1)[1]
            except IndexError:
                return await error_message(ctx.channel, "No arguments.")
            try:
                async with ClientSession() as session:
                    async with session.get(url) as resp:
                        json = await resp.text()
                        menu_list = loads(json)
            except InvalidURL:
                return await error_message(ctx.channel, "Invalid URL '{}'".format(url))
            except JSONDecodeError as exception:
                return await error_message(ctx.channel, "JSON Error: " + str(exception))
        elif sub == 'file':
            try:
                file = args.split(' ', 1)[1]
            except IndexError:
                return await error_message(ctx.channel, "No arguments.")
            if not file.endswith('.json'):
                file += '.json'
            try:
                with open('modules/embeds/' + file) as file:
                    try:
                        menu_list = loads(file.read())
                    except JSONDecodeError as exception:
                        return await error_message(ctx.channel, exception)
            except FileNotFoundError:
                return await error_message(ctx.channel, "Couldn't find file '{}'".format(file))
        else:
            if args.lstrip(' \t\r\n').startswith('```json') and args.endswith('```'):
                args = args.split('```json', 1)[1].rsplit('```', 1)[0]
            try:
                menu_list = loads(args)
            except JSONDecodeError as exception:
                return await error_message(ctx.channel, "JSON Error: " + str(exception))
        await self.post_menu(ctx, menu_list)

    async def post_menu(self, ctx, menu_list):
        # convert all content to messages
        if not isinstance(menu_list, list):
            menu_list = [menu_list]
        menu_dict = {}
        for content in menu_list:
            if not content:
                await ctx.channel.send('\u200b')
                continue
            embed = get_embed_from_json(content)
            message = await ctx.channel.send(embed=embed)
            content['message'] = message
            try:
                id = content.pop('id')
            except KeyError:
                id = message.id
            menu_dict[id] = content
            del embed
        # loop over messages and edit menus
        for id, content in menu_dict.items():
            if 'message-links' in content:
                i = 0
                desc = []
                for line, link in content['message-links'].items():
                    i+=1
                    try:
                        link = menu_dict[link]['message'].jump_url
                        desc.append("{0}. [{1}]({2})".format(i, line, link))
                    except:
                        desc.append("{}. ~~Message not found.~~".format(i))
                embed = get_embed_from_json(content)
                try:
                    embed.description = embed.description + '\n' + '\n'.join(desc)
                except:
                    embed.description = '\n'.join(desc)
                await message.edit(embed=embed)