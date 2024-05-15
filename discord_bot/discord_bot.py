import asyncio
from datetime import datetime
from invoice_generator import pdf_generator
import discord
import requests
from discord.ext import commands
import credentials

bot = discord.Bot()
bot.commands.clear()


# we need to limit the guilds for testing purposes
# so other users wouldn't see the command that we're testing

@bot.command(description="Get current medical dates")  # this decorator makes a slash command
async def get_dates(ctx):  # a slash coand will be created with the name "ping"
    await ctx.respond("get_dates was run")


# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} running together with FastAPI!")


class InvoiceGenerator:
    selection = {
        "schedule": {"Monday": "Canvas", "Tuesday": "Canvas", "Wednesday": "Cyrus", "Thursday": "Canvas", "Friday": "Canvas"},
        "invoice_week": "This week" if datetime.now().isoweekday() > 4 else "Last week"
    }

    class ScheduleConfirmationButtons(discord.ui.View):
        def __init__(self, *, timeout=None):
            super().__init__(timeout=timeout)
            self.add_item(discord.ui.Button(label="Okay", custom_id="okay", style=discord.ButtonStyle.green))
            self.add_item(discord.ui.Button(label="Not Okay", custom_id="not_okay", style=discord.ButtonStyle.red))

        async def interaction_check(self, interaction: discord.Interaction) -> bool:
            if interaction.data["custom_id"] == "okay":
                await interaction.response.send_message("Great! Generating your invoice...")
                schedule = InvoiceGenerator.selection['schedule']
                canvas_days = [day for day, company in schedule.items() if company == 'Canvas']
                cyrus_days = [day for day, company in schedule.items() if company == 'Cyrus']
                # print(canvas_days)
                # print(cyrus_days)
                # url = "http://127.0.0.1:8000"
                # payload = {"canvas_days": canvas_days, "cyrus_days": cyrus_days}
                # invoice_generate_url = "/invoice_generator/generate_invoice"
                # print("sending_request to generate")
                # print(requests.post(url + invoice_generate_url, params=payload))
                invoice_paths = pdf_generator.main(canvas_days, cyrus_days)
                print("request to generate sent")
                invoice_file_message  = await send_images(invoice_paths, 1187345577235730466)
                await invoice_file_message.add_reaction("📧")

                for item in self.children:
                    item.disabled = True
                await interaction.message.edit(view=self)

                return False
            elif interaction.data["custom_id"] == "not_okay":
                print("Confirmation declined")
                await interaction.message.delete()
                await interaction.response.send_message(view=InvoiceGenerator.ScheduleButtons())
                return False

    class ScheduleButtons(discord.ui.View):

        def __init__(self, *, timeout=None):
            super().__init__(timeout=timeout)
            self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            self.companies = ["Canvas", "Cyrus"]
            self.weeks = ["This week", "Last week"]

            # Create a button for each company for each day
            for day_index, day in enumerate(self.days):
                self.add_item(discord.ui.Button(label=day, disabled=True, row=day_index))

                for company_index, company in enumerate(self.companies):
                    style = discord.ButtonStyle.primary if InvoiceGenerator.selection["schedule"][
                                                               day] == company else discord.ButtonStyle.red
                    self.add_item(
                        discord.ui.Button(label=f"{company}", custom_id=f"{day}_{company}", style=style, row=day_index))

            for week_index, week in enumerate(self.weeks):
                style = discord.ButtonStyle.primary if InvoiceGenerator.selection["invoice_week"] == week else discord.ButtonStyle.red
                row = 0 if week == "This week" else 1
                self.add_item(discord.ui.Button(label=f"{week}", custom_id=f"week_{week}", style=style, row=row))

            # Add a "Done" button
            self.add_item(discord.ui.Button(label="Done", custom_id="done", style=discord.ButtonStyle.green, row=4))

        async def interaction_check(self, interaction: discord.Interaction):
            if interaction.data["custom_id"] == "done":
                schedule_selections = "\n".join(
                    f"{day}: {company}" for day, company in InvoiceGenerator.selection["schedule"].items() if company is not None)
                invoice_week = InvoiceGenerator.selection["invoice_week"]
                await interaction.response.send_message(
                    f"Schedule confirmed!\n{schedule_selections}\nInvoice Week: {invoice_week}", view=InvoiceGenerator.ScheduleConfirmationButtons())
                for item in self.children:
                    item.disabled = True
                await interaction.message.edit(view=self)
            elif "week" in interaction.data["custom_id"]:
                _, week = interaction.data["custom_id"].split('_')
                InvoiceGenerator.selection["invoice_week"] = week
                await interaction.response.defer()
                await interaction.message.edit(view=InvoiceGenerator.ScheduleButtons())
            else:
                day, company = interaction.data["custom_id"].split('_')
                InvoiceGenerator.selection["schedule"][day] = company
                await interaction.response.defer()
                await interaction.message.edit(view=InvoiceGenerator.ScheduleButtons())


@bot.event
async def on_reaction_add(reaction, user):
    reaction_channel_id = reaction.message.channel.id

    if user == bot.user:
        return

    if reaction_channel_id == 1187345577235730466:
        if str(reaction.emoji) == "👍":
            await reaction.message.channel.send("Select two companies for each weekday:", view=InvoiceGenerator.ScheduleButtons())


async def send_images(image_paths: list, channel_id: int):
    channel = bot.get_channel(channel_id)

    files = []
    for image_path in image_paths:
        filename = f"{image_path.split('/')[-1]}"  # Extract the filename from the path
        file = discord.File(image_path, filename=filename)
        files.append(file)
    message = await channel.send(files=files)

    return message




async def run():
    try:
        await bot.start(credentials.bot_token)  # Replace "token" with your actual bot token
    except KeyboardInterrupt:
        await bot.logout()


# Run the bot
# asyncio.run(run())
asyncio.create_task(run())

if __name__ == '__main__':
    bot.run(credentials.bot_token)
