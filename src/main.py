# Discord python bot for Konziis!
# 
# Python discord bot:
#   https://realpython.com/how-to-make-a-discord-bot-python/
#   https://discordpy.readthedocs.io/en/latest/index.html
#   https://github.com/Rapptz/discord.py/tree/v1.7.2/examples
# 
# Wolfram-API:
#   https://products.wolframalpha.com/api/documentation/#getting-started

import os
import random
import asyncio

import discord
from discord.ext import commands
from discord.ext import tasks

from mcstatus import MinecraftServer
import wolframalpha

from src.mycommands import MyCommands


TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
WOLFRAM_APPID = os.getenv('WOLFRAM_APPID')

MC_SERVER_CHECK_TIME = 10 * 60
MC_SERVER_ADDRESS = "ratius99.aternos.me"
MC_SERVER_STATUS_INT = 0

MESSAGE_CHANNEL = "📯mitteilungen"
TXT_VOICE_UPDATE = ["is needy and wait's for academic trash talk", 
                    "is lonely and want's to talk", 
                    "is waiting for you ",
                    "is sitting alone here",
                    "<put here some random text stuff>",
                    "wants to procrastinate",
                    "is dying of boredom",
                    "has a quarterlife-crisis"
                    ]

basic_activity_name =" in der Cloud! ☁"
bot = commands.Bot(command_prefix="!", activity= discord.Game(name=basic_activity_name))
wolframclient = wolframalpha.Client(WOLFRAM_APPID)

# Initialization errors

if not (TOKEN and GUILD and WOLFRAM_APPID):
    raise RuntimeError("Missing environmental variable.")


# Tasks

@tasks.loop(minutes=10)
async def check_mc_status():
    print("loopmc")

    mc_status = basic_activity_name
    players = 0
    
    try:
        server = MinecraftServer.lookup(MC_SERVER_ADDRESS)
        status = server.status()
        players = status.players.online
    except ConnectionRefusedError:
        mc_status = " mit Errors ..."
    except Exception:
        mc_status = " mit \"bad status error\" :-("

    # if no error happend:
    if (players):
        mc_status = " mit "+("einem Spieler" if (players==1) else str(players)+" Spielern")+" MC!"

    await bot.change_presence(activity = discord.Game(name=mc_status))


# Events

@bot.event 
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        channel_name=after.channel.name
        print("lonely state")
        await asyncio.sleep(10) # wait to est if user is shy / has misclicked
        if after.channel is not None:
            print("trigger")
            guild = discord.utils.get(bot.guilds, name=GUILD)
            voice_channel = discord.utils.get(guild.voice_channels, name=channel_name)
            print(voice_channel.voice_states)
            if len(voice_channel.voice_states)==1:
                print("t2")
                text_channel = discord.utils.get(guild.text_channels, name=MESSAGE_CHANNEL)
                await text_channel.send(f"Moin! {member.name} "+random.choice(TXT_VOICE_UPDATE)+". Visit him at #"+after.channel.name+".")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    check_mc_status.start()

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, hier ist der nerfffiger Diiscordbot aus Konziis!'
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # here read messageses   
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx: commands.Context, error):
    print(error.__cause__)
    await ctx.send(">> Error: "+str(error.__cause__))

bot.add_cog(MyCommands(bot, wolframclient))

bot.run(TOKEN)


# Custom event example:
# 
# bot.dispatch("custom_event", arg1, arg2)
#
# @bot.event
# async def on_custom_event(arg1, arg2):
#     print("Custom event")
