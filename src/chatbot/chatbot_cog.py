import discord
from discord.ext import commands

from chatbot import rara_chan

class ChatBot_(commands.Cog, name= "ChatBot"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["CHAT"])
    async def chat(self, ctx, *, question: str):
        '''
        Uses the ChatterBot library to generate responses
        '''

        response = rara_chan.answer(question)
        await ctx.reply(response)