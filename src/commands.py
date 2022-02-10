import json
import os
import random
import requests

import wolframalpha

from discord import Embed
from discord.ext import commands

from src.Configuration import Conf

AWS_SERVER_PUBLIC_KEY = os.getenv('AWS_SERVER_PUBLIC_KEY')
AWS_SERVER_SECRET_KEY = os.getenv('AWS_SERVER_SECRET_KEY')
WOLFRAM_APPID = os.getenv('WOLFRAM_APPID')
GUILD = os.getenv('DISCORD_GUILD')


class MainCommands(commands.Cog):
    """A couple of commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='random')
    async def random(self, ctx: commands.Context, number_of_dice: int, number_of_sides: int):
        """Simulates rolling dice."""
        print("random event!")

        embed = Embed(title="Zufallszahlen", color=random.choice(Conf.colors),
                      description=f"{number_of_dice} Würfel mit {number_of_sides} Seiten:")

        for _ in range(number_of_dice):
            w = str(random.choice(range(1, number_of_sides + 1)))
            embed.add_field(name=w, value="_" * len(w) + "/" + str(number_of_sides), inline=True)

        timeout = Conf.time_delete_random
        embed.set_footer(text=f"Selbstlöschend nach {timeout} Sekunden.")

        await ctx.message.delete()
        await ctx.send(embed=embed, delete_after=timeout)

    @commands.command(name='hi')
    async def hi(self, ctx: commands.Context, number_of_hi: int = 1):
        """Say \"Hi!\" multiple times."""
        print("hi!")

        for _ in range(number_of_hi):
            await ctx.send('Hi!')

    @commands.command(name='echo', help='Echo string.')
    async def echo(self, ctx: commands.Context, *, txt: str):
        """Echos input string."""
        print("echo!")

        await ctx.send(txt)

    @commands.command(name='emoji')
    async def emoji(self, ctx: commands.Context, emoji_name: str, image_url: str):
        """Creates custom server emoji. 
        Supports .jpg .gif .png."""
        print("emoji!")

        response = requests.get(image_url)
        img = response.content
        img = await ctx.guild.create_custom_emoji(name=emoji_name, image=img)

        await ctx.send(">> Emoji created: " + str(img))

    @commands.command(name='molec')
    async def molec(self, ctx: commands.Context, smile_string: str):
        """'Visualize a given molecule string. Supports MIME and other structural identifier.
        Note: Triple bonds in SMILES strings represented by \'\#\' have to be URL-escaped as \'%23\' and \'?\' as \'%3F\'."""
        print('molec!')

        url1 = 'http://cactus.nci.nih.gov/chemical/structure/' + smile_string + '/image'

        await ctx.send(">> Molecule: " + str(url1))


class WolframCommands(commands.Cog):
    """A couple of commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.wolframclient = wolframalpha.Client(WOLFRAM_APPID)

    @commands.command(name='wolfram')
    async def wolfram(self, ctx: commands.Context, *, question_string: str):
        """Use Wolfram Alpha (API) to solve Math or ask random stuff It can do ...
        everything WolframAlpha can do: Equations, Weather  (Overview: https://www.wolframalpha.com/)"""
        print('wolfram! ' + question_string)

        res = self.wolframclient.query(question_string)
        if not res.success:
            await ctx.send(">> Wolfram Weisnisch Weiter... ")
            return
        try:
            message = next(res.results).text
        except StopIteration:
            message = "No short result found. Try \"!wolfram-l\"."

        await ctx.send(">> Wolfram: " + message)

    @commands.command(name='wolfall')
    async def wolfall(self, ctx: commands.Context, *, question_string: str):
        """See !wolfram. Returns long informative answer"""
        print('wolfram! ' + question_string)

        res = self.wolframclient.query(question_string)
        if not res.success:
            await ctx.send(">> Wolfram Weisnisch Weiter... ")
            return

        message = ""
        for pod in res.pods:
            if pod.title == res.datatypes:
                message += str(pod.subpod.img.src) + "\n"
            for sub in pod.subpods:
                if sub.plaintext:
                    message += str(sub.plaintext) + "\n"

        await ctx.send(">> Wolfram: " + message)

    @commands.command(name='wolfget')
    async def wolfget(self, ctx: commands.Context, image_title: str, question_string: str):
        """See !wolfram. Returns image with given title"""
        print('wolfram! ' + question_string)

        res = self.wolframclient.query(question_string)
        if not res.success:
            await ctx.send(">> Wolfram Weisnisch Weiter... ")
            return

        message = ""
        try:
            message = next(res.results).text + "\n"
        except StopIteration:
            pass
        for pod in res.pods:
            if pod.title == image_title:
                message += str(pod.subpod.img.src) + "\n"

        await ctx.send(">> Wolfram: " + message)

class AWSCommands(commands.Cog):
    """Control Amazon ec2 server"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='todo', help='todo.')
    async def todo(self, ctx: commands.Context, *, txt: str):
        """todo."""
        print("todo!")

        await ctx.send(txt)
        
class QuotesCommands(commands.Cog):
    """ Quotes. """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    def get_random_quote(self) -> str:
        quotes = random.choice([Conf.quotes, Conf.quotes_better])
        quote = random.choice(quotes)
        return f">{['text']}\n>   ~{quote['author']}"

    @commands.command(name='quote', help='todo.')
    async def quote(self, ctx: commands.Context):
        """find a quote in quote colection"""
        print("quote!")
        
        await ctx.send(self.get_random_quote())
        
    @commands.command(name='findquote', help='todo.')
    async def findquote(self, ctx: commands.Context, *, search_phrase: str, printall: bool = False):
        """find a quote in quote colection"""
        print("findquote!")
        found_quotes = []
        
        for quotes in [Conf.quotes,Conf.quotes_better]:
            for quote in quotes:
                if search_phrase in quote["text"] or search_phrase in quote["author"]:
                    found_quotes.append(quote)
                    
        if found_quotes == []:
            quote = "Find nothing ..."
        elif printall:
            quote = "\n".join([f"\"{q['text']}\" ~ {q['author']};  " for q in found_quotes])
        else:
            quote = random.choice(found_quotes)
            
        await ctx.send(quote)
