from discord.ext import commands
from PIL import Image
import requests
import io
from image_detection.image_detection_module import predict

class Detect_Furry_(commands.Cog, name="Furry Detection"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["ISFURRY"])
    async def isfurry(self, ctx):
        ''' 
        Uses Keras' Sequential model to detect if an image is a furry or not
        '''

        attachments = ctx.attachments
        imgs = []
        for file in attachments:
            try:
                content = requests.get(file).content
                img = Image.open(io.BytesIO(content))
                
                idx = predict(img)

                if idx == 1:
                    await ctx.reply("I sense a Furry")
                    break
                else:
                    await ctx.reply("Normal shit")
            except Exception:
                continue


def setup(bot):
    bot.add_cog(Detect_Furry_(bot))
