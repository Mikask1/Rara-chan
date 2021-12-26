from random import randrange, choice
import os
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils import utilities

load_dotenv()

NO_REPLY_MENTION = discord.AllowedMentions(replied_user=False,)
TOKEN = os.getenv("TOKEN")

SEGS = ["SEEEGGGGGGSSS", "SEEEEEEEEGGGGGSSSS", "SEGGGGS", "AHHHH KIMOCHI SEGGGGGGGGGGS", "ORE WA SEGGGGS DAAA", "YAMERO TAKESHI, OMAE NO KARADA GA SEGGS DEKINAI", "IYAAA SEGGGS NI NARITAI, SEGGGGGGGGSSSS", "ORE WA ZETTAI NI SEEGGS NI NARUDA", "SEKKKUSU NI NARITAI", "ORE NO CHINCHIN GA FURUERU", "Betsuni SEGGGSSS suki tte wake janai ndakara, baka. BAAKAAAAA~~"]
GREETINGS = ["hewwo~", "H-hi", "H-hello", "Wassup ma boi", "What is it darling?", "Konnichiwa~", "Sekkusu shiyou ze", "Domoo~", "Iyaa~~ hanashikakenaide", "Kimoi", "Shine", "Baka", "Betsuni sukitte wake janai ndakara, baka", "...", "yada~ hanashitakunai", "urusai baka"]

class RaraChan(commands.Bot):
    def __init__(self) -> None:
        help_command = commands.DefaultHelpCommand(no_category = 'Help')
        super().__init__(command_prefix = "?", help_command=help_command)

        from nhentai.nhentai_cog import NHentai_
        from instagram.instagram_cog import Instagram_
        from nsfw.nsfw_cog import NFSW_
        from chatbot.chatbot_cog import ChatBot_
        from misc.misc_cog import Misc_

        self.add_cog(NHentai_(self))
        self.add_cog(Instagram_(self))
        self.add_cog(NFSW_(self))
        self.add_cog(ChatBot_(self))
        self.add_cog(Misc_(self))
        
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")

    async def on_message(self, ctx : str):
        if not ctx.author.bot:
            pp_message = ctx.content.lower().strip() # pre-processed ctx

            if ctx.author != self.user and utilities.in_oneWord(pp_message):
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

if __name__ == '__main__':
    rarachan = RaraChan()

    for i in rarachan.commands:
        print(i, i.signature)

    '''
    cog_name : cog
    qualified_name : name
    short doc : short desc.
    help: long desc.
    signature: ?get 
    '''

    rarachan.run()