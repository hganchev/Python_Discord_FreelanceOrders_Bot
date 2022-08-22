import discord
class Orders:
    def OrderOptions(self):
        return [discord.SelectOption(
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
                )]

    def PaymentMethods(self):
        return [discord.SelectOption(
                    label="Option 1",
                    value="1",
                    description="Pick this if you want [Payment 1]!"
                ),
                discord.SelectOption(
                    label="Option 2",
                    value="2",
                    description="Pick this if you want [Payment 2]!"
                ),
                discord.SelectOption(
                    label="Option 3",
                    value="3",
                    description="Pick this if you want [Payment 3]!"
                )]
