from typing import Optional
import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import OrderViews

### Set Global vars
load_dotenv()
GUILD_CHANNEL_ID = discord.Object(os.getenv('Guild_Id'))
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
        await self.tree.sync(guild=GUILD_CHANNEL_ID)

    async def on_member_join(self, member: Optional[discord.Member] = None):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Welcome {member.mention} to {guild.name}!'
            await guild.system_channel.send(to_send)

     
### Create Bot       
bot = MyClient()

### Client-bot Commands
## tree(guild) global (/command) commands
@bot.tree.command(guild=GUILD_CHANNEL_ID)
async def order(interaction: discord.Interaction):
    await interaction.response.send_modal(OrderViews.modalOrder())

@bot.tree.command(guild=GUILD_CHANNEL_ID)
async def offer(interaction: discord.Interaction):
    await interaction.response.send_modal(OrderViews.modalOffer())

### Run bot
bot.run(os.getenv('Discord_Token'))