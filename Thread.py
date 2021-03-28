import os
from discord.ext import commands
from discord import Embed, HTTPException
from utils import not_self, module_help
from json import load, dump

class Thread(commands.Cog):

    def __init__(self):
        if not os.path.isdir('modules/threads'):
            os.mkdir('modules/threads')
        self.thread_dict = {}
        for file in [file for file in os.listdir('modules/threads') if file.endswith('.json')]:
            with open('modules/threads/' + file, 'r') as json:
                self.thread_dict[file.rsplit('.json', 1)[0]] = load(json)['name']

    def help_message(self):
        return """Pretty much 4chan in Discord.
`{0} new (thread_name) [thread_message] [thread_author]`
\> Create a new thread.
`{0} reply (thread_name) [reply_message] [reply_author]`
\> Reply to an existing thread.
`{0} list`
\> Show a list of all existing threads.
`{0} show (thread_name)`
\> Displays a thread.
""".format(self.prefix + 'thread')

    @commands.command()
    @not_self()
    async def thread(self, ctx, *args):
        try:
            try:
                attachment = ctx.message.attachments[0].url
            except IndexError:
                attachment = None
            if args[0] == 'new':
                try:
                    await self.new(ctx.channel, args[1], args[2] if 2 < len(args) else None, args[3] if 3 < len(args) else None, attachment)
                except IndexError:
                    return await ctx.channel.send("Thread name can not be empty.")
            elif args[0] == 'reply':
                try:
                    await self.reply(ctx.channel, args[1], args[2] if 2 < len(args) else None, args[3] if 3 < len(args) else None, attachment)
                except IndexError:
                    return await ctx.channel.send("Thread name can not be empty.")
            elif args[0] == 'list':
                await self.list(ctx.channel)
            elif args[0] == 'show':
                try:
                    await self.show(ctx.channel, args[1])
                except IndexError:
                    await ctx.channel.send("Input a thread to show.")
            else:
                await module_help(ctx.channel, 'Thread', self.help_message())
        except IndexError:
            await module_help(ctx.channel, 'Thread', self.help_message())

    def get_id(self):
        if 'id' not in os.listdir('modules/threads'):
            with open('modules/threads/id', 'w+') as file:
                file.write('-1')
        with open('modules/threads/id', 'r') as file:
            this_id = str(int(file.read()) + 1)
        with open('modules/threads/id', 'w') as file:
            file.write(this_id)
            return this_id

    async def new(self, ctx, thread_name, thread_message, thread_author, attachment):
        if len(thread_name) > 50:
            return await ctx.send("Thread name needs to be shorter than 50 characters.")
        try:
            if len(thread_message) > 200:
                return await ctx.send("Message needs to be shorter than 200 characters.")
            if len(thread_author) > 20:
                 return await ctx.send("Your name needs to be shorter than 20 characters.")
        except TypeError:
            pass
        thread = {'name': thread_name, 'author': thread_author, 'message': thread_message, 'attachment': attachment, 'replies': []}
        id = self.get_id()
        with open('modules/threads/{0}.json'.format(id), 'w+') as file:
            dump(thread, file, indent=2)
            self.thread_dict[id] = thread_name
        await self.show(ctx, id)

    async def reply(self, ctx, id, reply_message, reply_author, attachment):
        if not reply_message:
            return await ctx.send('You can\'t reply with an empty message.')
        try:
            if len(reply_message) > 200:
                return await ctx.send("Message needs to be shorter than 200 characters.")
            if len(reply_author) > 20:
                 return await ctx.send("Your name needs to be shorter than 20 characters.")
        except TypeError:
            pass
        try:
            self.thread_dict[id]
        except:
            return await ctx.send("Couldn't find a thread with id '{}'.".format(id))
        with open('modules/threads/{0}.json'.format(id), 'r') as file:
            thread_dict = load(file)
        reply = {'author': reply_author, 'message': reply_message, 'attachment': attachment, 'id': self.get_id()}
        thread_dict['replies'].append(reply)
        with open('modules/threads/{0}.json'.format(id), 'w+') as file:
            dump(thread_dict, file, indent=2)
        await self.show(ctx, id)

    async def list(self, ctx):
        embed = Embed(title='Threads:')
        for id, thread in self.thread_dict.items():
            embed.add_field(name=thread, value='No. ' + id, inline=False)
        await ctx.send(embed=embed)

    async def show(self, ctx, id):
        try:
            thread = self.thread_dict[id]
        except:
            return await ctx.send("Couldn't find a thread with id '{}'.".format(id))
        with open('modules/threads/{0}.json'.format(id), 'r') as file:
            thread_dict = load(file)
        if thread_dict['author']:
            thread += ' - ' + thread_dict['author']
        else:
            thread += ' - Anonymous'
        thread += ' No.' + id
        desc = thread_dict['message'] or ''
        if thread_dict['attachment']:
            attachment = thread_dict['attachment']
            name = attachment.rsplit('/', 1)[1]
            if name.rsplit('.', 1)[1] in ['png', 'jpeg', 'jpg']:
                image = True
            else:
                desc += '\n[<{0}>]({1} "{1}")'.format(name, attachment)
        if desc:
            embed = Embed(title=thread, description=desc)
        else:
            embed = Embed(title=thread)
        try:
            if image:
                embed.set_thumbnail(url=attachment)
        except UnboundLocalError:
            pass
        for reply in thread_dict['replies']:
            if reply['author']:
                name = reply['author'] + ' No.' + reply['id']
            else:
                name = 'Anonymous No.' + reply['id']
            message = reply['message']
            if reply['attachment']:
                message += '\n[<{0}>]({1} "{1}")'.format(reply['attachment'].rsplit('/', 1)[1], reply['attachment'])
            embed.add_field(name=name, value=message, inline=False)
        try:
            await ctx.send(embed=embed)
        except HTTPException:
            await ctx.send("This thread is archived.")