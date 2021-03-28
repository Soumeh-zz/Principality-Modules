from discord.ext import commands
from discord import Embed
from utils import not_self, error_message, module_help
from json import load, dump

class To_Do(commands.Cog):
    def help_message(self):
        return """Keep tracks of things that you need to do.
`{0} add (task)`
\> Adds a task to your To-Do list.
`{0} list [member_name]`
\> Shows your [or someone else's] To-Do list.
`{0} remove (index)`
\> Removes a task at the index from your To-Do list.""".format(self.prefix + 'todo')
    @commands.command()
    @not_self()
    async def todo(self, ctx):
        try:
            args = ctx.message.content.split(' ', 1)[1]
        except IndexError:
            return await module_help(ctx.channel, self)
        todo_dict = self.get_todo_dict()
        sub = args.split()[0].lower()
        if sub == 'add':
            await self.add(ctx.message, args, todo_dict)
        elif sub == 'list':
            await self.list(ctx.message, args, todo_dict)
        elif sub == 'remove':
            await self.remove(ctx.message, args, todo_dict)
        else:
            await error_message(message.channel, "Invalid arguments")
    async def add(self, message, args, dict):
        try:
            arg = args.split(' ', 1)[1].replace('\n\n', '\n')
        except IndexError:
            return await error_message(message.channel, 'Task can not be empty.')
        try:
            dict[str(message.author.id)].append(arg)
        except:
            dict[str(message.author.id)] = [arg]
        embed = Embed(description='**Added** to your To-Do list:```diff\n+ {}```'.format(arg))
        await message.channel.send(embed=embed)
        self.save_todo_dict(dict)
    async def list(self, message, args, dict):
        try:
            arg = args.split(' ', 1)[1]
            member = message.guild.get_member_named(arg.split()[0])
            if not member:
                return await error_message(message.channel, 'Unknown member')
        except IndexError:
            member = message.author
        try:
            todo_list = dict[str(member.id)]
            if not todo_list:
                raise KeyError
        except KeyError:
            dict[str(member.id)] = []
            self.save_todo_dict(dict)
            return await error_message(message.channel, 'This To-Do list is empty')
        await self.send_todo(message.channel, message.author, todo_list)
    async def remove(self, message, args, dict):
        try:
            index = int(args.split(' ', 1)[1])
            if index > 0:
                index = index - 1
        except:
            return await error_message(message.channel, "Index can not be empty")
        try:
            todo_list = dict[str(message.author.id)]
            if not todo_list:
                raise IndexError
        except KeyError:
            dict[str(message.author.id)] = []
            self.save_todo_dict(dict)
            raise IndexError
        except IndexError:
            return await error_message(message.channel, "This To-Do list is empty")
        try:
            removed_value = todo_list.pop(index)
        except IndexError:
            return await error_message(message.channel, "Invalid Index")
        dict[str(message.author.id)] = todo_list
        self.save_todo_dict(dict)
        embed = Embed(description="**Removed** from your To-Do list:```diff\n- {}```".format(removed_value))
        await message.channel.send(embed=embed)
    def get_todo_dict(self):
        try:
            with open('modules/todos/todo.json', 'r+', encoding='utf-8') as file:
                return load(file)
        except FileNotFoundError:
            with open('modules/todos/todo.json', 'w+', encoding='utf-8') as file:
                file.write('{}')
            with open('modules/todos/todo.json', 'r+', encoding='utf-8') as file:
                return load(file)
    def save_todo_dict(self, dict):
        with open('modules/todos/todo.json', 'w+', encoding='utf-8') as file:
            dump(dict, file, indent=2)
    async def send_todo(self, channel, author, list):
        tasks = "<@{}>'s To-Do List:```ini\n".format(str(author.id))
        for index, task in enumerate(list, start=1):
            spaces = ' ' * (len(str(index)) + 3)
            tasks = tasks + '[{}] '.format(str(index)) + task.replace('\n','\n' + spaces) + '\n'
        tasks = tasks + '```'
        embed = Embed(description=tasks)
        await channel.send(embed=embed)