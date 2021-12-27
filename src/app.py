from random import randrange, choice
import os
from datetime import datetime

from discord.ui.button import Button
import discord
from discord import message
from discord import embeds
from discord.ext import commands, pages
from dotenv import load_dotenv

from utils import utilities
from utils.dropdown_pagination import DropdownPaginator

load_dotenv()

NO_REPLY_MENTION = discord.AllowedMentions(replied_user=False,)
TOKEN = os.getenv("TOKEN")

SEGS = ["SEEEGGGGGGSSS", "SEEEEEEEEGGGGGSSSS", "SEGGGGS", "AHHHH KIMOCHI SEGGGGGGGGGGS", "ORE WA SEGGGGS DAAA", "YAMERO TAKESHI, OMAE NO KARADA GA SEGGS DEKINAI", "IYAAA SEGGGS NI NARITAI, SEGGGGGGGGSSSS", "ORE WA ZETTAI NI SEEGGS NI NARUDA", "SEKKKUSU NI NARITAI", "ORE NO CHINCHIN GA FURUERU", "Betsuni SEGGGSSS suki tte wake janai ndakara, baka. BAAKAAAAA~~"]
GREETINGS = ["hewwo~", "H-hi", "H-hello", "Wassup ma boi", "What is it darling?", "Konnichiwa~", "Sekkusu shiyou ze", "Domoo~", "Iyaa~~ hanashikakenaide", "Kimoi", "Shine", "Baka", "Betsuni sukitte wake janai ndakara, baka", "...", "yada~ hanashitakunai", "urusai baka"]

class RaraChan(commands.Bot):
    def __init__(self, help_command) -> None:
        super().__init__(command_prefix = "?", help_command=help_command)
        cogs = utilities.get_cogs("src")
        for cog in cogs:
            self.load_extension(f"{cog[:-7]}.{cog[:-3]}")
        
    async def on_ready(self):
        self.profile_url = self.user.avatar.url
        print(f"Logged in as {self.user} (ID: {self.user.id})")

    async def on_message(self, ctx : str):
        if not ctx.author.bot:
            pp_message = ctx.content.lower().strip() # pre-processed ctx

            if ctx.author != self.user and utilities.in_oneWord(pp_message, "uwogh"):
                seggs = choice(SEGS)
                print(seggs)
                await ctx.reply(seggs)

            if "rara chan" == pp_message[:9] or "rara-chan" == pp_message[:9]:
                greet = choice(GREETINGS)
                print(greet)
                await ctx.reply(greet)

            if "yntkts" == pp_message:
                print("YNTKTS")
                await ctx.channel.send("https://i.ytimg.com/vi/rvUoEVeGmI8/maxresdefault.jpg")

            if "damn" in pp_message:
                damn = "d"+"a"*randrange(1, 5)+"y"*randrange(1, 10)+"u"*randrange(1,10)+"m"*randrange(1,10)
                print(damn)
                await ctx.reply(damn)
            
            if "no u" in pp_message:
                print("no u")
                await ctx.reply("no u")

            if randrange(500) == 3:
                print(ctx.author)
                await ctx.channel.send(f"Yadaa~~, <@{+ctx.author.id}> ga hentaiii~ (／≧ω＼). BAKAA!!")

            await self.process_commands(ctx)

    async def on_command(self, ctx):
        server = ctx.guild.name
        channel = ctx.channel
        user = ctx.author
        command = ctx.command
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        with open("logs.txt", "a", encoding="utf-8") as log:
            log.write(f"{date}: User {user} used ?{command} in #{channel} at [{server}]\n")
            
    def run(self):
        super().run(TOKEN)

class RaraHelpCommand(commands.DefaultHelpCommand):
    def __init__(self, **options):
        super().__init__(**options)

    async def send_bot_help(self, mapping):
        page_list = []
        options = []
        for cog in mapping:
            if cog == None: # No category
                continue

            embed = discord.Embed(title=cog.qualified_name, color=0x0080ff)
            
            embed.set_author(name="Rara-chan", icon_url=rarachan.profile_url)

            for command in cog.get_commands():
                embed.add_field(name="?"+command.qualified_name, value=command.short_doc, inline=False)

            embed.add_field(name="​​", value="﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏", inline=False)
            embed.set_footer(text="Type ?help command for more info on a command.\nYou can also type ?help category for more info on a category.")
            
            page_list.append(embed)
            
            options.append(discord.SelectOption(
                label=cog.qualified_name
                ))

        paginator = DropdownPaginator(pages=page_list, options=options, placeholder="Choose category..")
        
        await paginator.send(self.context)

    async def send_cog_help(self, cog):
        if cog == None: # No category
            await self.context.send("No such command exist")

        embed = discord.Embed(title=cog.qualified_name, color=0x0080ff)
        
        embed.set_author(name="Rara-chan", icon_url=rarachan.profile_url)

        for command in cog.get_commands():
            embed.add_field(name="?"+command.qualified_name, value=command.short_doc, inline=False)

        embed.add_field(name="​​", value="﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏", inline=False)
        embed.set_footer(text="Type ?help command for more info on a command.\nYou can also type ?help category for more info on a category.")

        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=group.qualified_name.upper(), color=0x0080ff)
        embed.set_author(name="Rara-chan", icon_url=rarachan.profile_url)

        embed.add_field(name="?"+group.qualified_name+" "+group.signature, value=group.short_doc, inline=False)

        subcommands = "\n?".join([command.qualified_name for command in group.commands])
        embed.add_field(name="sub-commands", value="?"+subcommands, inline=False)
        
        embed.add_field(name="​​", value="﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏", inline=False)
        embed.set_footer(text="Type ?help command for more info on a command.\nYou can also type ?help category for more info on a category.")

        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=command.qualified_name.upper(), color=0x0080ff)
        embed.set_author(name="Rara-chan", icon_url=rarachan.profile_url)

        embed.add_field(name="?"+command.qualified_name+""+command.signature, value="​​", inline=False)
        embed.add_field(name="Description", value=command.help, inline=False)
        
        embed.add_field(name="​​", value="﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏", inline=False)
        embed.set_footer(text="Type ?help command for more info on a command.\nYou can also type ?help category for more info on a category.")

        await self.context.send(embed=embed)

if __name__ == '__main__':
    rarachan = RaraChan(help_command=RaraHelpCommand(no_category="Help"))

    rarachan.run()
