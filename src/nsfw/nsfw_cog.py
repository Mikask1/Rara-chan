import time

import discord
from discord.ext import commands
from nsfw.nsfw_module import NSFW

class NSFW_(commands.Cog, name="NSFW"):
    def __init__(self, bot):
        self.bot = bot
        self.nsfw_ = NSFW()

    @commands.command(aliases = ["NSFW"])
    async def nsfw(self, ctx):
        '''
        Sends a random ZeroTwo NSFW from imagefap.com
        '''

        if not ctx.channel.is_nsfw():
            warning = await ctx.send("Please use the command in an NSFW channel")
            time.sleep(2)
            await warning.delete()
            return

        searching = await ctx.send('Searching...')
        print("Hornii")
        
        link = self.nsfw_.get_nsfw()
        embed = discord.Embed(title="Horny yet?", url=link, color=0xFF5733)
        embed.set_image(url=link)

        await searching.delete()
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(NSFW_(bot))