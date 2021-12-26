import time

import discord
from discord.ext import commands

from instagram.instagram_module import Post, Profile

class Instagram_(commands.Cog, name="Instagram"):
    def __init__(self, bot):
        self.bot = bot

    def _get_Post_embed(self, profile: Profile, post: Post, start_time: float):
        '''
        Gets the embed of a Post instance
        '''
        
        if not post: # if something went wrong while fetching the data
            return 0

        if post.media_type == "image":
            embed = discord.Embed(title=profile.username, url=post.url, color=0xFF5733)
            embed.set_image(url=post.media)
            embed.add_field(name="Caption:", value=post.caption, inline=False)
            embed.set_footer(text="Uploaded: "+post.upload_date+"\nExecution time: "+str((time.time() - start_time)))
            return embed

        elif post.media_type == "video":
            embed = discord.Embed(title=profile.username, url=post.url, color=0xFF5733)
            embed.add_field(name="Caption:", value=post.caption, inline=False)
            embed.set_footer(text="Uploaded: "+post.upload_date+"\nExecution time: "+str((time.time() - start_time)))
            return embed

    @commands.group(invoke_without_command= True)
    async def get(self, ctx, option, *, query: str):
        '''
        Get a post from an Instagram account

        Uses the instagram search bar if the profile link is not provided
        Get a random or indexed post (index 1) from the profile
        '''

        start_time = time.time()
        index = int(option)
        
        loading = await ctx.reply("Getting Profile..")
        profile = Profile(query)

        if not profile.exist: # if the search results has no results
            await ctx.reply("No results found")

        post = profile.get_post(index)

        if not post: # if it fails while fetching the data
            await ctx.reply("Sorry. Something went wrong")

        embed = self._get_Post_embed(profile, post, start_time)
    
        print(post.media)

        # Since embed can't store videos, we need to send the video first then the embed
        if post.media_type == "video":
            await ctx.send(post.media)

        await ctx.reply(embed=embed)
        await loading.delete()

    @get.command()
    async def random(self, ctx, *, query):
        start_time = time.time()
        loading = await ctx.reply("Getting Profile..")
        profile = Profile(query)

        if not profile.exist: # if the search results has no results
            await ctx.reply("No results found")
            
        post = profile.get_random_post()
        
        if not post: # if it fails while fetching the data
            await ctx.reply("Sorry. Something went wrong")

        embed = self._get_Post_embed(profile, post, start_time)

        # Since embed can't store videos, we need to send the video first then the embed
        if post.media_type == "video":
            await ctx.send(post.media)

        await ctx.reply(embed=embed)
        await loading.delete()

    @get.error
    async def get_error(self, ctx, error):
        error_message = 'Use format: `?get [<number> | "random"] [<query> | <url>]`\n\nFor example:\n```?get 1 real yami\n?get random https://www.instagram.com/real__yami/```'
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(error_message)
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.reply(error_message)