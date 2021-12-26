import time

import discord
from discord.ext import commands, pages

from nhentai.nhentai_module import NHentai
from utils import dropdown_pagination
from utils.dropdown_pagination import DropdownPaginator

# -- NHentai Cog --
class NHentai_(commands.Cog, name="NHentai"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.nhentai = NHentai()

    def _get_doujin_embed(self, doujin):
        '''
        Gets the embed form from the provided parameters from the Doujin instance
        '''

        embed = discord.Embed(title=doujin.title, url=doujin.url, color=0xFF5733)

        embed.add_field(name="ID", value=doujin.id, inline=True)
        
        # Only add English or Non-English
        for i in doujin.languages:
            if i == "english":
                embed.add_field(name="Language", value="English", inline=True)
                break
        else:
            embed.add_field(name="Language", value="Non-English", inline=True)

        embed.add_field(name="Page", value=doujin.pages, inline=True)

        if len(doujin.parodies) != 0:
            embed.add_field(name="Parodies", value=", ".join(doujin.parodies), inline=False)

        if len(doujin.characters) != 0:
            embed.add_field(name="Characters", value=", ".join(doujin.characters), inline=False)

        if len(doujin.tags) != 0:
            embed.add_field(name="Tags", value=", ".join(doujin.tags), inline=False)

        if len(doujin.artists) != 0:
            embed.add_field(name="Authors", value=", ".join(doujin.artists), inline=True)

        if len(doujin.groups) != 0:
            embed.add_field(name="Groups", value=", ".join(doujin.groups), inline=True)

        if doujin.cover != "":
            embed.set_image(url=doujin.cover)

        embed.set_footer(text = "Enjoy!")
        return embed

    @commands.command()
    async def id(self, ctx, code: str):
        '''
        Sends a doujin based on its ID on nhentai.net
        '''

        if not ctx.channel.is_nsfw():
            warning = await ctx.send("Please use the command in an NSFW channel")
            time.sleep(2)
            await warning.delete()
            return

            
        print("ID")
        searching = await ctx.send('Searching...')

        doujin = self.nhentai.get_doujin(id=code)
        
        if doujin.exist:
            embed = self._get_doujin_embed(doujin)

            await ctx.send(embed=embed)
        else:
            await ctx.send("No Results found")
        
        await searching.delete()

    @commands.command()
    async def search(self, ctx, *, query: str):
        '''
        Sends a random doujin based on the search query on nhentai.net
        '''
        
        if not ctx.channel.is_nsfw():
            warning = await ctx.send("Please use the command in an NSFW channel")
            time.sleep(2)
            await warning.delete()
            return


        print("Search", query)
        searching = await ctx.send('Searching...')

        doujins = self.nhentai.search(query=query+" english", size=10)
        if len(doujins): # Check if there are any results
            page_list = []
            options = []
            for n, link in enumerate(doujins, start=1):
                doujin = self.nhentai.get_doujin(link)
                options.append(discord.SelectOption(
                    label="Page "+str(n), 
                    description="ID: "+str(doujin.id)
                    ))
                embed = self._get_doujin_embed(doujin)
                page_list.append(embed)
            
        
            paginator = DropdownPaginator(page_list, "Choose Page..", options=options)

            paginator.customize_button("next", button_label=">", button_style=discord.ButtonStyle.green)
            paginator.customize_button("prev", button_label="<", button_style=discord.ButtonStyle.green)
            paginator.customize_button("first", button_label="<<", button_style=discord.ButtonStyle.blurple)
            paginator.customize_button("last", button_label=">>", button_style=discord.ButtonStyle.blurple)

            await paginator.send(ctx)
        else:
            await ctx.send(embed= discord.Embed(title="No results found"))

        await searching.delete()

    @commands.command()
    async def random(self, ctx):
        '''
        Sends a random doujin from nhentai.net
        '''
        
        if not ctx.channel.is_nsfw():
            warning = await ctx.send("Please use the command in an NSFW channel")
            time.sleep(2)
            await warning.delete()
            return


        print("Random")
        searching = await ctx.send('Searching...')

        doujin = self.nhentai.random()
        embed = self._get_doujin_embed(doujin)
        
        await searching.delete()
        await ctx.send(embed=embed)

    @commands.command()
    async def popular(self, ctx):
        '''
        Sends the popular page doujins from nhentai.net
        '''


        if not ctx.channel.is_nsfw():
            warning = await ctx.send("Please use the command in an NSFW channel")
            time.sleep(2)
            await warning.delete()
            return

        searching = await ctx.send('Searching...')

        print("Popular")
        links = self.nhentai.popular()
        
        page_list = []
        options = []
        for n, link in enumerate(links, start=1):
            doujin = self.nhentai.get_doujin(link)
            options.append(discord.SelectOption(
                label="Page "+str(n), 
                description="ID: "+str(doujin.id)
                ))
            embed = self._get_doujin_embed(doujin)
            page_list.append(embed)
    
        paginator = DropdownPaginator(page_list, "Choose Page..", options=options)

        paginator.customize_button("next", button_label=">", button_style=discord.ButtonStyle.green)
        paginator.customize_button("prev", button_label="<", button_style=discord.ButtonStyle.green)
        paginator.customize_button("first", button_label="<<", button_style=discord.ButtonStyle.blurple)
        paginator.customize_button("last", button_label=">>", button_style=discord.ButtonStyle.blurple)
        
        await searching.delete()
        await paginator.send(ctx)
