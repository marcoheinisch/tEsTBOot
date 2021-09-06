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
from src.Configuration import Conf


class ServerStat:
    stopping = "stopping"
    offline = "offline"
    starting = "starting"
    online = "online"
    error = "error"
    none = None


TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
AWS_SERVER_PUBLIC_KEY = os.getenv('AWS_SERVER_PUBLIC_KEY')
AWS_SERVER_SECRET_KEY = os.getenv('AWS_SERVER_SECRET_KEY')

session = boto3.Session(
    aws_access_key_id=AWS_SERVER_PUBLIC_KEY,
    aws_secret_access_key=AWS_SERVER_SECRET_KEY,
    region_name="eu-central-1"
)

intents = discord.Intents.default()
intents.reactions = True
bot = commands.Bot(command_prefix="!", activity=discord.Game(name=Conf.activity_name_basic), intents=intents)


async def update_status_channel(known_awsstat=ServerStat.none):
    channel = bot.get_channel(Conf.channel_status)

    if known_awsstat:
        player, serverstat = 0, known_awsstat
    else:
        player, serverstat = get_mc_status(Conf.mc_server_amazon)

    controller_message = \
        "-> Kontrolliere hier mit Reaktionen den tEsTOot:\n" \
        " 1) Starte (:white_check_mark:) und stoppe (:x:) den Amazon Minecraftserver .\n" \
        " 2) mal sehn'... \n" \
        "-> Serverstatus: \n" \
        f" - Amazon 17.1 (ip: 3.125.141.61): {serverstat}, {player} Spieler \n" \
        " - Aternos 17.1 (-): siehe Bot-Status\n" \
        " - Aternos 16.X (-): siehe #minecraft-log-1-16 "
    msg = await channel.fetch_message(Conf.massage_status)
    await msg.edit(content=controller_message)

    name = f"↪🔄{serverstat}"
    if serverstat == ServerStat.offline:
        name = "↪❌offline"
    if serverstat == ServerStat.online:
        name = "↪✅online"
    await channel.edit(name=name)

    return serverstat


def get_mc_status(ip: str):
    players = 0
    serverstat = ServerStat.offline
    try:
        server = MinecraftServer.lookup(ip)
        status = server.status()
        players = int(status.players.online)
    except Exception:
        serverstat = ServerStat.offline
    if players:
        serverstat = ServerStat.online

    return players, serverstat


# Tasks

@tasks.loop(minutes=Conf.time_check_mcserver)
async def check_mc_status():
    print("loopmc")

    players, serverstat = get_mc_status(Conf.mc_server_aternos1)

    mc_status = Conf.activity_name_basic
    if serverstat == ServerStat.error:
        mc_status = " mit Error - _ -"
    if serverstat == ServerStat.online:
        mc_status = " mit " + ("einem Spieler" if (players == 1) else f"{players} Spielern") + " MC!"

    await bot.change_presence(activity=discord.Game(name=mc_status))


@tasks.loop(seconds=Conf.time_check_mcserver_seconds, count=Conf.count_check_aws_mcserver)
async def check_aws_mc_status():
    print("loopawsmc")

    p, serverstat = get_mc_status(Conf.mc_server_amazon)

    if serverstat == ServerStat.online:
        check_aws_mc_status.stop()
        await update_status_channel(ServerStat.online)


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
                text_channel = discord.utils.get(guild.text_channels, id=Conf.channel_welcome)
                await text_channel.send(f"Moin! {member.name} " + random.choice(
                    Conf.welcome_text) + ". Visit him at #" + after.channel.name + ".")


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    check_mc_status.start()
    await update_status_channel()


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
    if payload.message_id == Conf.massage_status:
        print(f"reaction {payload.emoji.name}")

        ec2 = session.resource('ec2')
        instance = ec2.Instance(Conf.ec2_instance_id)

        if payload.emoji.name == "✅":
            try:
                instance.start()
                await update_status_channel(known_awsstat=ServerStat.starting)
                instance.wait_until_running()
                check_aws_mc_status.start()
            except Exception as e:
                print(e)
                await update_status_channel(known_awsstat=ServerStat.error)

        if payload.emoji.name == "❌":
            try:
                instance.stop()
                await update_status_channel(known_awsstat=ServerStat.stopping)
                instance.wait_until_stopped()
                await update_status_channel(known_awsstat=ServerStat.offline)
            except Exception as e:
                print(e)
                await update_status_channel(known_awsstat=ServerStat.error)

        if payload.emoji.name == "⏪":
            pass
            # ec2.modify_instance_attribute(InstanceId=Conf.ec2_instance_id, Attribute='instanceType', Value='t2.small')

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
