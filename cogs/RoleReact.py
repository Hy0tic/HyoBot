from discord.ext import commands
import discord.utils

class RoleReact(commands.Cog):
  def __init__(self, BOT):
    self.BOT = BOT
  
  @commands.Cog.listener()
  async def on_ready(self):
    print('RoleReact cog ready') 

  @commands.command(name="CreateReactionRoleMessage", help="create message to give server members roles")
  async def CreateReactionRoleMessage(self,ctx):
    commandAuthor = ctx.author
    await ctx.send("Hello, which channel would you like the message in?")

    async def handleChannel(message):
        if message.author != commandAuthor:
            return

        channel_ids = [int(c.strip('<>#')) for c in message.content.split() if c.startswith('<#') and c.endswith('>')]  # Extract channel IDs from message
        channels = [discord.utils.get(ctx.guild.channels, id=id) for id in channel_ids]  # Find channels with given IDs
        print(channels[0])
        selectedChannel = channels[0]

        self.BOT.remove_listener(handleChannel, 'on_message')
        await ctx.send("The channel is " + message.content + " what would you like the message to say? Use a | to separate the title from the description like so\n ```This is the title | this is the description```\n You can also type `{roles}` to list out all of the roles and their emoji")
        self.BOT.add_listener(handleReactionMessage, 'on_message')

    async def handleReactionMessage(message):
        if message.author != commandAuthor:
            return

        parts = message.split(' | ')
        title = parts[0]
        description = parts[1]

        # define the message where user would get role
        if(description == "{roles}"):
            pass # list all roles and their emojies
        else:
            pass # message title and description

        await ctx.send(f"Alright I got the title and the description:\n ```{message.content}```\n Would you like the message to have a color?")


        print("handling reaction message")
        self.BOT.remove_listener(handleReactionMessage, 'on_message')
        await ctx.send("The format for adding roles is emoji then name of the role. when you're done, type 'done'")
        self.BOT.add_listener(handleRoleCreation, 'on_message')
    
    async def handleRoleCreation(message):
        if message.author != commandAuthor:
            return
        color = message.content

    self.BOT.add_listener(handleChannel, 'on_message')

async def setup(BOT):
  await BOT.add_cog(RoleReact(BOT))  