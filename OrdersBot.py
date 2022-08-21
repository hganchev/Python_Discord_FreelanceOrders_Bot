from typing import Optional
import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import OrderViews

### Set Client
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

    async def on_joined(interaction: discord.Interaction, member: Optional[discord.Member] = None):
        member = member or interaction.user
        await interaction.response.send_message(f'{member} joined {discord.utils.format_dt(member.joined_at)}')
        await interaction.response.send_message(f'Hello {member} to my Discord Server!')

     
### Create Bot       
load_dotenv()
bot = MyClient()

### Client-bot Commands
## tree(guild) global (/command) commands
@bot.tree.command(guild=discord.Object(952610014370099240))
async def order(interaction: discord.Interaction):
    view = OrderViews.Order()
    await interaction.response.send_message(view = view, ephemeral=True)

@bot.tree.command(guild=discord.Object(952610014370099240))
async def offer(interaction: discord.Interaction):
    view = OrderViews.Offer()
    await interaction.response.send_message(view = view, ephemeral=True)

@bot.tree.command(guild=discord.Object(952610014370099240))
async def modal(interaction: discord.Interaction):
    await interaction.response.send_modal(OrderViews.modalOrder())

### Run bot
bot.run(os.getenv('Discord_Token'))