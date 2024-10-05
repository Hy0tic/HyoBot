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
    custom_emojis = re.findall(r'<a?:[^\s<>:]+:\d+>', msg)
    pattern = r'<a?:([^\s<>:]+):(\d+)>'
    emojiList = []
    for emoji in custom_emojis:
        match = re.match(pattern, emoji)
        if match:
            name = match.group(1)
            emoji_id = match.group(2)
            animated = emoji.startswith('<a:')
            emojiList.append([name, emoji_id, animated])

    print(emojiList)

    try:
        os.makedirs("./cogs/TempImageFolder")
    except:
        pass

    for emoji in emojiList:
        name = emoji[0]
        emojiId = emoji[1]
        isAnimated = emoji[2]

        extension = ".gif" if isAnimated else ".png"
        urlExtension = ".gif" if isAnimated else ".webp"
        url = "https://cdn.discordapp.com/emojis/" + emojiId + urlExtension
        print("url:" + url)
        path = "./cogs/TempImageFolder"

        filename = name + extension
        try:
          download_image(url, path, filename)
        except:
          await ctx.send(f"{ctx.author.mention} Failed to download emoji")
          return

        server = ctx.guild
        try: 
          with open("./cogs/TempImageFolder/" + filename, "rb") as file:
              emoji_data = file.read()
        except:
          await ctx.send(f"{ctx.author.mention} Failed to read file")
          os.remove("./cogs/TempImageFolder/" + filename)
          return
           
        try:
          await server.create_custom_emoji(name=name, image=emoji_data)
          await ctx.send(f"{ctx.author.mention} Emoji Created")
        except:
          await ctx.send(f"{ctx.author.mention} Failed to create emoji")

        os.remove("./cogs/TempImageFolder/" + filename)
        
async def setup(BOT):
  await BOT.add_cog(Emoji(BOT))  

def download_image(url, save_directory, file_name):
    response = requests.get(url)
    response.raise_for_status()  # Check for any errors during the request

    save_path = os.path.join(save_directory, file_name)

    with open(save_path, "wb") as file:
        file.write(response.content)