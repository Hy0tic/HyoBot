from discord.ext import commands
from asyncio import sleep as s

class Remind(commands.Cog):
  def __init__(self, BOT):
    self.BOT = BOT
  
  @commands.Cog.listener()
  async def on_ready(self):
    print('Remind cog ready') 

  @commands.command(help="reminder")
  async def remind(self,ctx,num,unit,objective = ""):
#    ctx.author.id
    if unit == 'sec' or unit == 'second' or unit == 'seconds' :
      await ctx.send(f"{ctx.author.mention} " + "Reminder in " + num + " second(s)" + ": " + str(objective))
      await s(int(num))
      await ctx.send(f'{objective}, {ctx.author.mention}')
    elif unit == 'min' or unit == 'minute' or unit == 'minutes' :
      await ctx.send(f"{ctx.author.mention} " + "Reminder in " + num + " minute(s)" + ": " + str(objective))
      await s(int(num)*60)
      await ctx.send(f'{objective}, {ctx.author.mention}')
    elif unit == 'hr' or 'hrs' or unit == 'hour' or unit == 'hours':
      await ctx.send(f"{ctx.author.mention} " + "Reminder in " + num + " hour(s)" + ": " + str(objective))
      await s(int(num)*60*60)
      await ctx.send(f'{objective}, {ctx.author.mention}')
    elif unit == 'day' or unit == 'days':
      await ctx.send(f"{ctx.author.mention} " + "Reminder in " + num + " day(s)" + ": " + str(objective))
      await s(int(num)*60*60*24)
      await ctx.send(f'{objective}, {ctx.author.mention}')
    elif unit == 'year' or unit == 'years':
      await ctx.send()

async def setup(BOT):
  await BOT.add_cog(Remind(BOT))  