import discord
import discord.interactions
from Orders import Orders
from discord import SelectMenu, SelectOption
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
OrdersClass = Orders()

### set discord bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.dm_messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

###
class Order(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=5)

    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose an Order Option!",
        min_values = 1,
        max_values = 1,
        options = OrdersClass.OrderOptions()
    )
    async def select_Order(
        self, 
        interaction: discord.Interaction, 
        select: discord.ui.Select):
        select.disabled = True
        await interaction.message.reply(f"Nice! You Selected {select.values[0]}")
        await interaction.response.edit_message(view = self)

    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a Payment method!",
        min_values = 1,
        max_values = 1,
        options = OrdersClass.PaymentMethods()
    )
    async def select_Payment(
        self, 
        interaction: discord.Interaction, 
        select: discord.ui.Select):
        select.disabled = True
        await interaction.message.reply(f"Nice! You Selected {select.values[0]}")
        await interaction.response.edit_message(view = self)

    @discord.ui.button(
        label="Make an Order", 
        style=discord.ButtonStyle.green)
    async def button_MakeOrder(
        self,
        interaction: discord.Interaction, 
        button: discord.ui.Button):
        button.disabled = True
        await interaction.message.reply("Your order is beeing sent for processing...")
        await interaction.response.edit_message(view = self)

class Offer(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=5)
    
    @discord.ui.button(
        label="Accept Offer", 
        style=discord.ButtonStyle.green,
        row=1)
    async def button_AcceptOffer(
        self,
        interaction: discord.Interaction, 
        button: discord.ui.Button):
        button.disabled = True
        await interaction.message.reply("The order is beeing accepted")
        await interaction.response.edit_message(view = self)
        #await interaction.data.copy - copy the response and save

    @discord.ui.button(
        label="Decline Offer", 
        style=discord.ButtonStyle.red,
        row=1)
    async def button_DeclineOffer(
        self,
        interaction: discord.Interaction, 
        button: discord.ui.Button):
        button.disabled = True
        await interaction.message.reply("The order is beeing declined")
        await interaction.response.edit_message(view = self)

### Client-bot commands
@bot.command()
async def order(ctx):
    view = Order()
    await ctx.reply(view = view)

@bot.command()
async def offer(ctx):
    view = Offer()
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