import discord
from socket import timeout
from Orders import Orders
from datetime import datetime
### Reference to Orders
OrdersClass = Orders()

### Views and Modals
## Order View
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

## Offer View
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

## Order Modal
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
            timestamp= datetime.now(),
            color=discord.Color.blue())
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed = embed)