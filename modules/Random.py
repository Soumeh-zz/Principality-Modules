from discord.ext import commands
from utils import not_self, module_help
from random import choice

class Random(commands.Cog):
    keywords = {
        "prefix": ['Dumb', 'Random', 'Annoying', 'Round', 'Tiny', 'Gay', 'Inconsequential', 'Uncalled For', 'Pedantic', 'Based'],
        "color":  ['Blue', 'Black', 'White', 'Green', 'Red', 'Yellow', 'Purple', 'Cyan', 'Navy', 'Brown'],
        "object": ['Ball', 'Book', 'Bimbo', 'Bird', 'Bitch', 'Baby', 'Rat', 'Sword', 'Scythe', 'Bow', 'E-Girl', 'Blanket', 'Bottle', 'Cake', 'Door', 'Table', 'Glass', 'Window', 'Bread', 'Bee', 'Dog', 'Horse', 'Rock', 'Crystal', 'Gun', 'Chewing Gum', 'Cigarette', 'Cigar', 'CD', 'Phone', 'Axe', 'Stick', 'Car', 'Worm', 'Cloth', 'Toy', 'Bat', 'Snake', 'Cat', 'Closet', 'Mirror', 'MILF', 'DILF', 'Soup', 'Popcorn', 'Bowl', 'Flag', 'Carpet', 'Dress', 'Hair', 'Camera', 'Chair', 'TV', 'Toilet', 'Chimney', 'Furnace', 'Chest', 'Pickaxe', 'Hoe', 'Crossbow', 'Cape', 'Apple', 'Pie', 'Wire', 'Wine', 'Gasoline', 'Champagne', 'Lasagna', 'Spaghetti', 'Skeleton', 'Zombie', 'Vampire', 'Buffalo', 'Angel', 'Demon', 'The Holy Bable', 'Fingernail', 'Toenail', 'Button', 'Knife', 'Dagger', 'Lighter', 'Lightbulb', 'Pepper Spray', 'Koala', 'Tiger', 'Lion', 'Leaf', 'Alpaca', 'Zebra', 'Dolphin', 'Plankton', 'Weed', 'Flower', 'Clock', 'Tooth', 'Teeth', 'Sheep', 'Wolf', 'Fox', 'Ocelot', 'Turtle', 'Tower', 'Train', 'Sun', 'Moon', 'Star', 'Crab', 'Pen', 'Paper', 'Scissors', 'Pineapple', 'Egg', 'Salad', 'Whip', 'Noose', 'Crown', 'Glasses', 'Pony', 'Mask', 'Tissue', 'Sunglasses', 'Drill', 'Hammer', 'Bucket', 'Bag', 'Can', 'Toaster', 'Fridge', 'Ashtray', 'Helmet', 'Towel', 'Armor', 'Shoe', 'Shoes', 'Ant', 'Spider', 'Ladybug', 'Chicken', 'Squid', 'Snail', 'Butterfly', 'Kangaroo'],
        "suffix": ['of The Damned', 'of Epicness', 'of Randomness', 'of Complete Madness', 'of the Cringe', '', 'of the Rat King']
    }
    def help_message(self):
        return """Returns a message with any keywords replaced with random words.
`{0} (arguments)`
\> Returns a string with any keywords in (arguments) replaced with random words.
  Keywords: {1}""".format(self.prefix + 'random', ', '.join(['[' + keyword + ']' for keyword in self.keywords.keys()]))
    @commands.command()
    @not_self()
    async def random(self, ctx):
        try:
            args = ctx.message.content.split(' ', 1)[1]
        except IndexError:
            return await module_help(ctx.channel, self)
        for keyword, list in self.keywords.items():
            keyword = '[' + keyword + ']'
            while keyword in args:
                args = args.replace(keyword, choice(list), 1)
        await ctx.channel.send(args)