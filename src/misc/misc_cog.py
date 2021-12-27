import discord
from discord.ext import commands

from app import NO_REPLY_MENTION

class Misc_(commands.Cog, name="Misc"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        '''
        Sends the bot's ping
        '''
        
        await ctx.send(f'Ping = {round(self.bot.latency * 1000)} ms')

    @commands.command()
    async def seggs(self, ctx):
        '''
        Sends the "japanese man running through a tunnel yelling seggs" clip
        '''

        print("SEGGGGGGGGGSSSSSSSS")
        await ctx.reply("https://cdn.discordapp.com/attachments/903149126353575956/910047595454398485/seggs.mp4", allowed_mentions=NO_REPLY_MENTION)
    
def setup(bot):
    bot.add_cog(Misc_(bot))