import discord
import os
from discord.ext import commands
from dotenv import load_dotenv


# client = discord.Client(intents=discord.Intents.default())
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.dm_messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=0)

    @discord.ui.button(label="Make Order", style=discord.ButtonStyle.green)
    async def menuOrder(self,interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.reply('Order in progress')

### Client-bot commands
@bot.command()
async def menu(ctx):
    view = Menu()
    await ctx.reply(view = view)
###

### Client-bot events
## Ready
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

## Member Join
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )
###

bot.run(os.getenv('Discord_Token'))