from dis import disco
import time
import asyncio

import discord
from discord.ext import commands

from instagram.instagram_module import Post, Profile, create_profile
from utils.dropdown_pagination import DropdownPaginator

class Instagram_(commands.Cog, name="Instagram"):
    def __init__(self, bot):
        self.bot = bot

    def _get_Media_embed(self, username: str, post: Post, media: Post.Media, start_time: float):
        '''
        Gets the embed of a Post instance
        '''
        
        embed = discord.Embed(title=username, url=post.url, color=0xFF5733)

        if media.media_type == "image":
            embed.set_image(url=media.url)

        embed.add_field(name="Caption:", value=post.caption, inline=False)
        embed.set_footer(text="Uploaded: "+post.upload_date+f"\nExecution time: {int(time.time() - start_time)} seconds")
        return embed

    def _get_Carousel_embed(self, username: str, posts: Post, start_time: float) -> DropdownPaginator:
        page_list = []
        options = []

        for n, media in enumerate(posts.media, start=1):
            options.append(discord.SelectOption(
                label=f"Slide {n}"
            ))
            if media.media_type == "image":
                embed = self._get_Media_embed(post=posts, username=username, media=media, start_time=start_time)
                page_list.append(embed)
    
        paginator = DropdownPaginator(page_list, "Choose Page..", options=options)

        paginator.customize_button("next", button_label=">", button_style=discord.ButtonStyle.green)
        paginator.customize_button("prev", button_label="<", button_style=discord.ButtonStyle.green)
        paginator.customize_button("first", button_label="<<", button_style=discord.ButtonStyle.blurple)
        paginator.customize_button("last", button_label=">>", button_style=discord.ButtonStyle.blurple)

        return paginator

    @commands.group(invoke_without_command= True)
    async def get(self, ctx: discord.abc.Messageable, option, *, query: str):
        '''
        Get a post from an Instagram account

        Uses the instagram search bar if the profile link is not provided
        Get a random or indexed post (index 1) from the profile
        '''

        # Fix Post Class
        start_time = time.time()
        index = int(option)
        
        loading = await ctx.reply("Getting Profile..")
        profile = await create_profile(query)

        if not profile.exist: # if the search results has no results
            await ctx.reply("No results found")

        await loading.edit(content="Getting post..")
        url = await profile.get_post(index)

        if not url: # if it fails while fetching the data
            await ctx.reply("Sorry. Something went wrong")

        task = asyncio.create_task(profile.get_properties(url))

        post = await task
        if post.is_carousel:
            paginator = self._get_Carousel_embed(posts=post, username=profile.username, start_time=start_time)
            await loading.delete()
            await paginator.send(ctx)
        else:
            embed = self._get_Media_embed(post=post, username=profile.username, media=post.media, start_time=start_time)
            if post.media.media_type == "video":
                await loading.edit(content=post.media.url, embed=embed)
            else:
                await loading.edit(content="", embed=embed)

    @get.command()
    async def random(self, ctx: discord.abc.Messageable, *, query):
        '''
        Gets a random post from an Instagram account
        '''
        start_time = time.time()
        loading = await ctx.reply("Getting Profile..")
        profile = await create_profile(query)

        if not profile.exist:
            await ctx.reply("No results found")

        await loading.edit(content="Getting post..")  
        post = await profile.get_random_post()
        
        if not post:
            await ctx.reply("Sorry. Something went wrong")

        embed = self._get_Post_embed(profile, post, start_time)
        if post.is_video:
            await loading.edit(content=post.media)
            await ctx.send(embed=embed)
        else:
            await loading.edit(content="", embed=embed)

    @get.error
    async def get_error(self, ctx, error):
        error_message = 'Use format: `?get [<number> | "random"] [<query> | <url>]`\n\nFor example:\n```?get 1 real yami\n?get random https://www.instagram.com/real__yami/```'
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(error_message)
        if isinstance(error, commands.errors.CommandInvokeError):
            print(error)
            await ctx.reply(error_message)

def setup(bot):
    bot.add_cog(Instagram_(bot))