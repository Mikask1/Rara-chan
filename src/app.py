from random import randrange, choice
import time
import os

import discord
from discord.ext import commands, pages
from dotenv import load_dotenv

from utils import utilities
from nhentai.nhentai import NHentai
from nsfw.nsfw import NSFW
from instagram.instagram_scraper import Profile
from chatbot import rara_chan

load_dotenv()

NO_REPLY_MENTION = discord.AllowedMentions(replied_user=False,)
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix = "?")

SEGS = ["SEEEGGGGGGSSS", "SEEEEEEEEGGGGGSSSS", "SEGGGGS", "AHHHH KIMOCHI SEGGGGGGGGGGS", "ORE WA SEGGGGS DAAA", "YAMERO TAKESHI, OMAE NO KARADA GA SEGGS DEKINAI", "IYAAA SEGGGS NI NARITAI, SEGGGGGGGGSSSS", "ORE WA ZETTAI NI SEEGGS NI NARUDA", "SEKKKUSU NI NARITAI", "ORE NO CHINCHIN GA FURUERU", "Betsuni SEGGGSSS suki tte wake janai ndakara, baka. BAAKAAAAA~~"]
GREETINGS = ["hewwo~", "H-hi", "H-hello", "Wassup ma boi", "What is it darling?", "Konnichiwa~", "Sekkusu shiyou ze", "Domoo~", "Iyaa~~ hanashikakenaide", "Kimoi", "Shine", "Baka", "Betsuni sukitte wake janai ndakara, baka", "...", "yada~ hanashitakunai", "urusai baka"]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

# RESPOND TO CERTAIN MESSAGES
@bot.event
async def on_message(message : str):
    if not message.author.bot:
        pp_message = message.content.lower().strip() # pre-processed message

        if message.author != bot.user and utilities.in_oneWord(pp_message):
            seggs = choice(SEGS)
            print(seggs)
            await message.reply(seggs)

        if "rara chan" == pp_message[:9] or "rara-chan" == pp_message[:9]:
            greet = choice(GREETINGS)
            print(greet)
            await message.reply(greet)

        if "yntkts" == pp_message:
            print("YNTKTS")
            await message.channel.send("https://i.ytimg.com/vi/rvUoEVeGmI8/maxresdefault.jpg")

        if "damn" in pp_message:
            damn = "d"+"a"*randrange(1, 5)+"y"*randrange(1, 10)+"u"*randrange(1,10)+"m"*randrange(1,10)
            print(damn)
            await message.reply(damn)
        
        if "no u" in pp_message:
            print("no u")
            await message.reply("no u")

        if randrange(500) == 3:
            print(message.author)
            await message.channel.send(f"Yadaa~~, <@{+message.author.id}> ga hentaiii~ (／≧ω＼). BAKAA!!")

        await bot.process_commands(message)


# -- NHentai Cog --

class Nhentai_(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.nhentai = NHentai()

    @commands.command()
    async def id(self, message, code : str):
        '''
        Sends a doujin based on its ID on nhentai.net

        Command : ?id <id>
        '''

        if message.channel.is_nsfw():
            print("ID")
            searching = await message.send('Searching...')

            doujin = self.nhentai.get_doujin(id=code)
            
            if doujin.valid:
                embed = utilities.get_doujin_embed(doujin)

                await message.send(embed=embed)
            else:
                await message.send("No Results found")
            
            await searching.delete()
        else:
            warning = await message.send("Please use the command in an NSFW channel")
            time.sleep(2)
            await warning.delete()

    @commands.command()
    async def search(self, message, *, query):
        '''
        Sends a random doujin based on the search query on nhentai.net
        
        Command : ?search <query>
        '''

        if message.channel.is_nsfw():
            print("Search", query)
            searching = await message.send('Searching...')
            doujins = self.nhentai.search(query=query+" english")
            
            if len(doujins) != 0:
                page_list = []
                for links in doujins:
                    doujin = self.nhentai.get_doujin(links)
                    embed = utilities.get_doujin_embed(doujin)
                    page_list.append(embed)
                
                paginator = pages.Paginator(pages=page_list, show_disabled=True, show_indicator=True)

                paginator.customize_button("next", button_label=">", button_style=discord.ButtonStyle.green)
                paginator.customize_button("prev", button_label="<", button_style=discord.ButtonStyle.green)
                paginator.customize_button("first", button_label="<<", button_style=discord.ButtonStyle.blurple)
                paginator.customize_button("last", button_label=">>", button_style=discord.ButtonStyle.blurple)

                await paginator.send(message)
            else:
                await message.send(embed= discord.Embed(title="No results found"))

            await searching.delete()
        else:
            warning = await message.send("Please use the command in an NSFW channel")
            time.sleep(2)
            await warning.delete()

    @commands.command()
    async def random(self, message):
        '''
        Sends a random doujin from nhentai.net
        
        Command : ?random
        '''
        
        if message.channel.is_nsfw():
            print("Random")
            searching = await message.send('Searching...')
            doujin = self.nhentai.random()

            if doujin.valid:
                embed = utilities.get_doujin_embed(doujin)
                
                await message.send(embed=embed)
            else:
                await message.send("No Results found")
            
            await searching.delete()
        else:
            warning = await message.send("Please use the command in an NSFW channel")
            time.sleep(2)
            await warning.delete()

    @commands.command()
    async def popular(self, message):
        '''
        Sends the popular page doujins from nhentai.net
        
        Command : ?popular (<index>)
        '''


        if message.channel.is_nsfw():
            print("Popular")

            page_list = []
            links = self.nhentai.popular()
            
            for i in range(len(links)):
                doujin = self.nhentai.get_doujin(links[i])
                embed = utilities.get_doujin_embed(doujin)
                page_list.append(embed)

            paginator = pages.Paginator(pages=page_list, show_disabled=True, show_indicator=True)

            paginator.customize_button("next", button_label=">", button_style=discord.ButtonStyle.green)
            paginator.customize_button("prev", button_label="<", button_style=discord.ButtonStyle.green)
            paginator.customize_button("first", button_label="<<", button_style=discord.ButtonStyle.blurple)
            paginator.customize_button("last", button_label=">>", button_style=discord.ButtonStyle.blurple)
            
            await paginator.send(message)


# -- NSFW Cog --
class NFSW_(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nsfw_ = NSFW()

    @commands.command(aliases = ["NSFW"])
    async def nsfw(self, message):
        '''
        Sends a random ZeroTwo NSFW from imagefap.com
        
        Command : ?nsfw
        '''

        if message.channel.is_nsfw():
            link = self.nsfw_.get_nsfw()
            
            print("Hornii")
            embed = discord.Embed(title="Horny yet?", url=link, color=0xFF5733)
            embed.set_image(url=link)

            await message.reply(embed=embed)
        else:
            warning = await message.send("Please use the command in an NSFW channel")
            time.sleep(2)
            await warning.delete()

# -- Instagram Cog --
class Instagram_(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def get(self, message, *, args):
        '''
        Get a post from an Instagram account

        Uses the instagram search bar if the profile link is not provided
        Get a random or indexed post (index 1) from the profile

        command = ?get [<number> | "random"] [<query> | <url>]
        '''

        start_time = time.time()
        argv = args.split()

        if len(argv) >= 2:
            query = " ".join(argv[1:])

            loading = await message.reply("Getting Profile..")
            profile = Profile(query)

            if profile.valid:
                await loading.edit(content="Getting Post..")
                if argv[0] == "random":
                    post = profile.get_random_post()
                    embed = utilities.ig_post_embed(profile, post, start_time)
                    if embed != -1:
                        print(post.media)
                        if post.media_type == "video":
                            await message.send(post.media)
                        await message.reply(embed=embed)
                    else:
                        await message.reply("No post found or <number> exceeded 12")
                else:
                    try:
                        index = int(argv[0])
                        post = profile.get_post(index)
                        embed = utilities.ig_post_embed(profile, post, start_time)
                        if embed != -1:
                            print(post.media)
                            if post.media_type == "video":
                                await message.send(post.media)
                            await message.reply(embed=embed)
                        else:
                            await message.reply("No post found or <number> exceeded 12")
                    except ValueError:
                        await message.reply('Use format: `?get [<number> | "random"] [<query> | <url>]`\n\nFor example:\n```?get 1 real yami\n?get random https://www.instagram.com/real__yami/```')
                await loading.delete()
            else:
                await message.reply("No results found")
        else:
            await message.reply('Use format: `?get [<number> | "random"] [<query> | <url>]`\n\nFor example:\n```?get 1 real yami\n?get random https://www.instagram.com/real__yami/```')


# -- ChatBot Cog --
class ChatBot_(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["CHAT"])
    async def chat(self, message, *, arg):
        '''
        Uses the ChatterBot library to generate responses

        Command : ?chat <question>
        '''

        response = rara_chan.answer(arg)
        await message.reply(response)


# -- Misc. Commands Cog --
class Misc_(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, message):
        await message.send(f'Ping = {round(bot.latency * 1000)} ms')

    @commands.command(aliases= ["SEGGS"])
    async def seggs(self, message):
        '''
        Sends the "japanese man running through a tunnel yelling seggs" clip

        Command : ?seggs
        '''

        print("SEGGGGGGGGGSSSSSSSS")
        await message.reply("https://cdn.discordapp.com/attachments/903149126353575956/910047595454398485/seggs.mp4", allowed_mentions=NO_REPLY_MENTION)

bot.add_cog(Nhentai_(bot))
bot.add_cog(Instagram_(bot))
bot.add_cog(NFSW_(bot))
bot.add_cog(ChatBot_(bot))
bot.add_cog(Misc_(bot))

bot.run(TOKEN)