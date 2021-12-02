import discord
from discord.ext import commands
import random
import os

description = '''Tony bot commands'''

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', description=description, intents=intents )
treat_count = 0

@bot.command()
async def meow( ctx ):
    emote = random.choice( ["<:tonyaah:860900789925183518>", "<:tonyhappy:860900538317406218>"])
    await ctx.send( emote + ' meow ' + emote )

@bot.command()
async def moew( ctx ):
    emote = random.choice( ["<:tonyaah:860900789925183518>", "<:tonyhappy:860900538317406218>"])
    await ctx.send( emote + ' moew ' + emote )

@bot.command()
async def tonypic( ctx ):
    pic = random.choice(open('pic-links.txt').read().splitlines())
    await ctx.send(pic)

@bot.command()
async def treat( ctx ):
    global treat_count
    treat_count += 1
    await ctx.send( f"<:tonyhappy:860900538317406218> <:tonyhappy:860900538317406218> <:tonyhappy:860900538317406218> meow onm onm onm onm meow <:tonyhappy:860900538317406218> <:tonyhappy:860900538317406218> <:tonyhappy:860900538317406218>\n\t\t\t\tJ'en ai mangé {treat_count} aujourd'hui.")

bot.run(open('token.txt').read())