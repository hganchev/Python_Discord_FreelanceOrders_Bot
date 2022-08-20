import discord
import discord.interactions
from discord import SelectMenu, SelectOption
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

class Order(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=0)

    @discord.ui.button(label="Make Order", style=discord.ButtonStyle.green)
    async def menuOrder(self,interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.reply("You are in orders")
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose an Order Option!",
        min_values = 1,
        max_values = 1,
        options = [
                discord.SelectOption(
                    label="Option 1",
                    description="Pick this if you want [Option 1]!"
                ),
                discord.SelectOption(
                    label="Option 2",
                    description="Pick this if you want [Option 2]!"
                ),
                discord.SelectOption(
                    label="Option 3",
                    description="Pick this if you want [Option 3]!"
                )
            ]
    )
    async def select_Order(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_message(f"Nice! You Selected {select.values[0]}")

### Client-bot commands
@bot.command()
async def order(ctx):
    view = Order()
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