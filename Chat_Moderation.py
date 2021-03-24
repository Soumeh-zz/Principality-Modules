from discord.ext import commands
from discord.errors import Forbidden
from start import prefix
from utils import not_self, embed_message
from re import sub
from json import load

class Chat_Moderation(commands.Cog):

    # Config
    mod_messages_channel = 802584493843546132 # where to send notifications about moderation
    moderated_servers = [802577295960571907]
    moderated_channels = [802993783692066836, 802584493843546132] # set to '*' for every channel to be moderated
    unmoderated_channels = [802584493843546132]
    default_name = 'Charlie' # renames a member if they have a blacklisted name

    # Config End
    def __init__(self):
        if isinstance(self.moderated_channels, list):
            [self.moderated_channels.pop(self.moderated_channels.index(channel)) for channel in self.unmoderated_channels if channel in self.moderated_channels]
        with open('modules/blacklists/blacklist.json', 'r') as blacklist_json:
            self.blacklist = load(blacklist_json)
    async def __asinit__(self):
        self.mod_messages_channel = await self.bot.fetch_channel(self.mod_messages_channel)
    def help_message(self):
        return """Moderates content sent by members.
\> Deletes blacklisted words.
\> Notifies about blacklisted names."""

    @commands.Cog.listener()
    async def on_message(self, message):
        if (self.moderated_channels == '*' and message.channel.id not in self.unmoderated_channels) or message.channel.id in self.moderated_channels:
            if self.is_blacklisted(message.content):
                message_copy = message
                await message.delete()
                await self.warning('send', message_copy)
    @commands.Cog.listener()
    async def on_message_edit(self, old, new):
        if (self.moderated_channels == '*' and message.channel.id not in self.unmoderated_channels) or old.channel.id in self.moderated_channels:
            if self.is_blacklisted(new.content):
                message_copy = new
                await new.delete()
                await self.warning('edit', message_copy)
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.is_blacklisted(member.name):
            member_copy = member
            try:
                await member.edit(nick=self.default_name)
            except Forbidden:
                pass
            await self.warning('username', user)
        if self.is_blacklisted(member.raw_status):
            await self.warning('status', user)
    @commands.Cog.listener()
    async def on_member_update(self, old, new):
        if new.nick == old.nick:
            return
        if self.is_blacklisted(new.nick):
            member_copy = new
            try:
                await new.edit(nick=old.nick, reason='Blacklisted Content')
            except Forbidden:
                return
            await self.warning('nickname', member_copy)
        if self.is_blacklisted(new.raw_status):
            await self.warning('status', user)

    def is_blacklisted(self, string):
        if not string:
            return False
        string = sub('[^0-9a-zA-Z ]+', '', string.lower())
        string_split = string.split(' ')
        for full in self.blacklist['full']:
            if full in string_split:
                return full
        for word in string_split:
            for start in self.blacklist['start']:
                if word.startswith(start) and word != start:
                    return start
            for end in self.blacklist['end']:
                if word.endswith(end) and word != end:
                    return end
        for partial in self.blacklist['partial']:
            if partial in string:
                return partial
        return None

    async def warning(self, reason, content):
        if reason == 'send':
            await self.mod_messages_channel.send('User sent a message containing blacklisted content.')
            await embed_message(self.mod_messages_channel, content)
        elif reason == 'edit':
            await self.mod_messages_channel.send('User edited a message containing blacklisted content.')
            await embed_message(self.mod_messages_channel, content)
        elif reason == 'username':
            await self.mod_messages_channel.send('User <@{}> joined with a nickname containing blacklisted content.'.format(content.id))
        elif reason == 'nickname':
            await self.mod_messages_channel.send('User <@{}> set a nickname containing blacklisted content.'.format(content.id))
        elif reason == 'status':
            await self.mod_messages_channel.send('User <@{}> has a custom status containing blacklisted content.'.format(content.id))