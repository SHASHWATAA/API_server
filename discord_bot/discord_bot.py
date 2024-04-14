import asyncio

import discord
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

async def run():
    try:
        await bot.start(credentials.bot_token)  # Replace "token" with your actual bot token
    except KeyboardInterrupt:
        await bot.logout()


# Run the bot
asyncio.create_task(run())


if __name__ == '__main__':
    bot.run(credentials.bot_token)
