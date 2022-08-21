import datetime
from socket import timeout
from turtle import title
import discord
import discord.interactions
from Orders import Orders
from discord import SelectMenu, SelectOption
from discord import app_commands
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
OrdersClass = Orders()

class MyClient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        intents.dm_messages = True
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        await self.tree.sync(guild=discord.Object(952610014370099240))

    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!'
        )

bot = MyClient()

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
        self.button_DeclineOffer.disabled = True
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
        self.button_AcceptOffer.disabled = True
        button.disabled = True
        await interaction.message.reply("The order is beeing declined")
        await interaction.response.edit_message(view = self)

class modalOrder(discord.ui.Modal, title='Example'):
    def __init__(self):
        super().__init__(timeout=5)

    OrderSpec = discord.ui.TextInput(
        label= "add order specification", 
        style=discord.TextStyle.long,
        placeholder="What the project contains, what is about?")
    
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title= self.title, 
            description=f"Description: {self.OrderSpec.value}",
            timestamp= datetime.datetime.now(),
            color=discord.Color.blue())
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed = embed)

### Client-bot tree(guild) global (/command) commands
@bot.tree.command(guild=discord.Object(952610014370099240))
async def order(interaction: discord.Interaction):
    view = Order()
    await interaction.response.send_message(view = view, ephemeral=True)

@bot.tree.command(guild=discord.Object(952610014370099240))
async def offer(interaction: discord.Interaction):
    view = Offer()
    await interaction.response.send_message(view = view, ephemeral=True)

@bot.tree.command(guild=discord.Object(952610014370099240))
async def modal(interaction: discord.Interaction):
    await interaction.response.send_modal(modalOrder())
###

bot.run(os.getenv('Discord_Token'))