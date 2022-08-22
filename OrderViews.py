import discord
from Orders import Orders
from datetime import datetime
### Reference to Orders
OrdersClass = Orders()

### Views and Modals
## Order Modal
class modalOrder(discord.ui.Modal, title='Order'):
    def __init__(self):
        super().__init__(timeout=10)

    # Name
    Name = discord.ui.TextInput(
        label='Name',
        style=discord.TextStyle.short,
        placeholder="What is your name?"
    )
    # Email
    Email = discord.ui.TextInput(
        label='Email',
        style=discord.TextStyle.short,
        placeholder="What is your email?"
    )
    # Order Specifications
    OrderSpec = discord.ui.TextInput(
        label="Add Order Specification", 
        style=discord.TextStyle.long,
        placeholder="What the project contains, what is about?"
    )
    # Attachments
    AttachedFileName = discord.ui.TextInput(
        label="Add file path", 
        style=discord.TextStyle.short,
        placeholder="What the project contains, what is about?"
    )
    
    # Submit 
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=self.title, 
            description=f"Description: {self.OrderSpec.value}",
            timestamp=datetime.now(),
            color=discord.Color.blue())
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        # try taking file name, extension(pdf,txt,etc.)
        file = discord.File(fp=self.AttachedFileName.value, filename='OrderSpec.pdf')
        await interaction.response.send_message(embed = embed, file=file)

## Offer Modal
class modalOffer(discord.ui.Modal, title='Offer'):
    def __init__(self):
        super().__init__(timeout=10)
    # Select Order
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose an Order!",
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

    # Name 

    # Email

    # Offer Description

    # Submit
        

## Order View
class ViewOrder(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=5)

    @discord.ui.button(
        label="Make an Offer", 
        style=discord.ButtonStyle.green)
    async def button_MakeOffer(
        self,
        interaction: discord.Interaction, 
        button: discord.ui.Button):
        interaction.guild = discord.Object(952610014370099240)
        button.disabled = True
        await interaction.message.reply("Your offer is beeing sent for processing...")
        await interaction.response.edit_message(view = self)

## Offer View
class ViewOffer(discord.ui.View):
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

## Modal Accept Offer
class modalAcceptOffer(discord.ui.Modal):
    def __init__(self):
        super().__init__(timeout=5)

    # Payment method
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
        interaction.guild = discord.Object(952610014370099240)
        select.disabled = True
        await interaction.message.reply(f"Nice! You Selected {select.values[0]}")
        await interaction.response.edit_message(view = self)