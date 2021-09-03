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

import boto3
from mcstatus import MinecraftServer
from src.commands import MainCommands, WolframCommands

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
AWS_SERVER_PUBLIC_KEY = os.getenv('AWS_SERVER_PUBLIC_KEY')
AWS_SERVER_SECRET_KEY = os.getenv('AWS_SERVER_SECRET_KEY')

MC_SERVER_CHECK_TIME = 10  # minutes
MC_SERVER_ADDRESS = "ratius99.aternos.me"
MC_SERVER_STATUS_INT = 0
REACTION_MESSAGE_ID = 883455925090930728

MESSAGE_CHANNEL = "📯mitteilungen"
TXT_VOICE_UPDATE = ["is needy and wait's for academic trash talk",
                    "is lonely and want's to talk",
                    "is waiting for you ",
                    "is sitting alone here",
                    "wants to procrastinate",
                    "is dying of boredom",
                    "has a quarterlife-crisis",
                    "is plotting to overthrow the government.",
                    "is hiding a bomb bellow his desk."
                    ]

conf = {
    "timeout_random": 60,
    "aws_mc_checktime": 1,
    "aws_mc_server_adress": "3.125.141.61",
    "status_channel": 852114543759982592,
    "status_massage": 883455925090930728
}

intents = discord.Intents.default()
intents.reactions = True
basic_activity_name = " in der Cloud! ☁"
bot = commands.Bot(command_prefix="!", activity=discord.Game(name=basic_activity_name), intents=intents)

controller_message = "Kontrolliere hier mit Reaktionen den tEsTOot:\n 1) Starte mit :white_check_mark: und stoppe mit :x: einen Amazon Minecraftserver (ip: 3.125.141.61).\n 2) mal sehn'..."


# Tasks

@tasks.loop(minutes=MC_SERVER_CHECK_TIME)
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

    if players:  # if no error happend:
        mc_status = " mit " + ("einem Spieler" if (players == 1) else str(players) + " Spielern") + " MC!"

    await bot.change_presence(activity=discord.Game(name=mc_status))


# Events

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        channel_name = after.channel.name
        print("lonely state")
        await asyncio.sleep(10)  # wait to est if user is shy / has misclicked
        if after.channel is not None:
            print("trigger")
            guild = discord.utils.get(bot.guilds, name=GUILD)
            voice_channel = discord.utils.get(guild.voice_channels, name=channel_name)
            print(voice_channel.voice_states)
            if len(voice_channel.voice_states) == 1:
                print("t2")
                text_channel = discord.utils.get(guild.text_channels, name=MESSAGE_CHANNEL)
                await text_channel.send(f"Moin! {member.name} " + random.choice(
                    TXT_VOICE_UPDATE) + ". Visit him at #" + after.channel.name + ".")


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    check_mc_status.start()

    channel = bot.get_channel(conf["status_channel"])
    channel.send(controller_message)
    msg = await channel.fetch_message(REACTION_MESSAGE_ID)
    await msg.edit(content=controller_message)
    await msg.add_reaction('❌')
    await msg.add_reaction('✅')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, hier issst der nerfffiger Diiscordbot aus Konziis!'
    )


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # here read messages
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx: commands.Context, error):
    print(error.__cause__)
    await ctx.send(">> Error: " + str(error.__cause__))


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == REACTION_MESSAGE_ID:
        print(f"reaction {payload.emoji.name}")

        session = boto3.Session(
            aws_access_key_id=AWS_SERVER_PUBLIC_KEY,
            aws_secret_access_key=AWS_SERVER_SECRET_KEY,
            region_name="eu-central-1"
        )
        ec2 = session.resource('ec2')
        instance = ec2.Instance('i-07baa970d1c82bb08')

        channel = bot.get_channel(conf["status_channel"])

        if payload.emoji.name == "✅":
            try:
                instance.start()
                await channel.edit(name=f"✅-aws-starting")
            except Exception as e:
                print(e)

        if payload.emoji.name == "❌":
            try:
                instance.stop()
                await channel.edit(name='❌-aws-stopping')
            except Exception as e:
                print(e)

        if payload.emoji.name == "⏪":
            pass

        if payload.emoji.name == "⏩":
            pass

bot.add_cog(MainCommands(bot))
bot.add_cog(WolframCommands(bot))

bot.run(TOKEN)

# Custom event example:
# 
# bot.dispatch("custom_event", arg1, arg2)
#
# @bot.event
# async def on_custom_event(arg1, arg2):
#     print("Custom event")
