from discord.ext import commands
import re
import discord
import requests
import os

class Emoji(commands.Cog):
  def __init__(self, BOT):
    self.BOT = BOT

  @commands.Cog.listener()
  async def on_ready(self):
    print('Emoji cog ready') 

  @commands.command(help="steal")
  async def steal(self, ctx, msg):
    custom_emojis = re.findall(r'<:\w*:\d*>', msg)

    emojiList = []

    for string in custom_emojis:
        # Extract the content within the arrow braces using regular expressions
        match = re.search(r'<:(.*):(.*)>', string)
        
        if match:
            # Retrieve the captured groups from the match object
            group1 = match.group(1)
            group2 = match.group(2)
            
            # Append the formatted parts to the new list
            emojiList.append([group1, group2])

    os.makedirs("./cogs/TempImageFolder")
    for emoji in emojiList:
        name = emoji[0]
        emojiId = emoji[1]
        
        url = "https://cdn.discordapp.com/emojis/" + emojiId + ".webp?size=40&quality=lossless"
        path = "./cogs/TempImageFolder"
        filename = name + ".png"
        download_image(url, path, filename)

        server = ctx.guild
        with open("./cogs/TempImageFolder/" + filename, "rb") as file:
            emoji_data = file.read()
        await server.create_custom_emoji(name=name, image=emoji_data)
        os.remove("./cogs/TempImageFolder/" + filename)
        
async def setup(BOT):
  await BOT.add_cog(Emoji(BOT))  

def download_image(url, save_directory, file_name):
    response = requests.get(url)
    response.raise_for_status()  # Check for any errors during the request

    save_path = os.path.join(save_directory, file_name)

    with open(save_path, "wb") as file:
        file.write(response.content)