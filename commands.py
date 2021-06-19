from discord.ext import commands

import random
import requests
import wolframalpha

class Commands(commands.Cog):
    """A couple of commands."""

    def __init__(self, bot: commands.Bot, wolframclient):
        self.bot = bot
        self.wolframclient = wolframclient


    @commands.command(name='roll_dice')
    async def roll(self, ctx: commands.Context, number_of_dice: int, number_of_sides: int):
        """Simulates rolling dice."""
        print("roll event!")

        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        print(dice)
        await ctx.send(', '.join(dice))


    @commands.command(name='hi')
    async def roll(self, ctx: commands.Context, number_of_hi: int = 1):
        """Say \"Hi!\" multiple times."""
        print("hi!")

        for _ in range(number_of_hi):
            await ctx.send('Hi!')


    @commands.command(name='echo', help='Echo string.')
    async def roll(self, ctx: commands.Context, *, txt:str):
        """Echos input string."""
        print("echo!")

        await ctx.send(txt)


    @commands.command(name='emoji')
    async def roll(self, ctx: commands.Context, emoji_name: str, image_url:str):
        """Creates custom server emoji. 
        Supports .jpg .gif .png."""
        print("emoji!")

        response = requests.get(image_url)
        img = response.content   
        img = await ctx.guild.create_custom_emoji(name=emoji_name, image=img)
        await ctx.send(">> Emoji created: "+str(img))


    @commands.command(name='molec')
    async def roll(self, ctx: commands.Context, smile_string: str):
        """'Visualize a given molecule string. Supports MIME and other structural identifier. 
        Note: Triple bonds in SMILES strings represented by \'\#\' have to be URL-escaped as \'%23\' and \'?\' as \'%3F\'."""
        print('molec!')

        url1 = 'http://cactus.nci.nih.gov/chemical/structure/' + smile_string+ '/image'
        await ctx.send(">> Molecule: "+ str(url1))
        

    @commands.command(name='wolfram')
    async def roll(self, ctx: commands.Context, *, question_string: str):
        """Use Wolfram Alpha (API) to solve Math or ask random stuff It can do ...
        everything WolframAlpha can do: Equations, Weather  (Overview: https://www.wolframalpha.com/)"""
        print('wolfram! ' + question_string)

        res = self.wolframclient .query(question_string)
        if not res.success:
            await ctx.send(">> Wolfram Weisnisch Weiter... ")
            return
        try:
            message = next(res.results).text
        except StopIteration:
            message = "No short result found. Try \"!wolfram-l\"."
        await ctx.send(">> Wolfram: "+ message)


    @commands.command(name='wolfall')
    async def roll(self, ctx: commands.Context, *, question_string: str):
        """See !wolfram. Returns long informative answer"""
        print('wolfram! ' + question_string)

        res = self.wolframclient .query(question_string)
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
        await ctx.send(">> Wolfram: "+ message)


    @commands.command(name='wolfget')
    async def roll(self, ctx: commands.Context, image_title: str, question_string: str):
        """See !wolfram. Returns image with given title"""
        print('wolfram! ' + question_string)

        res = self.wolframclient .query(question_string)
        if not res.success:
            await ctx.send(">> Wolfram Weisnisch Weiter... ")
            return

        message = ""    
        try:
            message = next(res.results).text+"\n"
        except StopIteration:
            pass
        for pod in res.pods:
            if pod.title == image_title:
                message += str(pod.subpod.img.src) + "\n"
        await ctx.send(">> Wolfram: "+ message)

