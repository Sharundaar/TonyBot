import discord
from discord.ext import commands
import random
from datetime import date

description = '''Tony bot commands'''

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', description=description, intents=intents )
pic_links = []
treats_per_day = {}

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
    global pic_links
    pic = random.choice(pic_links)
    await ctx.send(pic)

@bot.command()
async def treat( ctx ):
    global treats_per_day
    today = date.today().strftime("%d/%m/%Y")
    if today not in treats_per_day:
        treats_per_day[today] = 0
    treats_per_day[today] += 1
    treat_count = treats_per_day[today]
    with open( 'treat-count.txt', 'w' ) as f:
        for k, v in treats_per_day.items():
            f.write( f'{k} {v}\n' )
    await ctx.send( f"<:tonyhappy:860900538317406218> <:tonyhappy:860900538317406218> <:tonyhappy:860900538317406218> meow onm onm onm onm meow <:tonyhappy:860900538317406218> <:tonyhappy:860900538317406218> <:tonyhappy:860900538317406218>\n\t\t\t\tJ'en ai mangé {treat_count} aujourd'hui.")

@bot.command()
async def tonysleep( ctx ):
    await ctx.send( "<:zzzztony:890679784349265931><:zzzztony:890679784349265931> it is late meow, go to sleep <:zzzztony:890679784349265931><:zzzztony:890679784349265931>\n<:zzzztony:890679784349265931><:zzzztony:890679784349265931> it is late meow, go to sleep <:zzzztony:890679784349265931><:zzzztony:890679784349265931>\n<:zzzztony:890679784349265931><:zzzztony:890679784349265931> it is late meow, go to sleep <:zzzztony:890679784349265931><:zzzztony:890679784349265931>")

@bot.command()
async def addpic( ctx, link ):
    global pic_links
    pic_links.append( link )
    with open( 'pic-links.txt', 'w' ) as f:
        f.write( '\n'.join( pic_links ) ) 
        await ctx.send("J'ai ajouté cette image dans ma mémoire <:tonyhappy:860900538317406218>")

@bot.command()
async def removepic( ctx, link ):
    global pic_links
    try:
        pic_links.remove( link )
        with open( 'pic-links.txt', 'w' ) as f:
            f.write( '\n'.join( pic_links ) ) 
        await ctx.send("J'ai enlevé l'image de ma mémoire <:tonyhappy:860900538317406218>")
    except ValueError:
        await ctx.send("Je n'ai pas cette image dans ma mémoire <:tonysad:860900605383147551>")


@bot.event
async def on_disconnect():
    print( "Meow! Going to sleep..." )

@bot.event
async def on_ready():
    print("Meow! I'm awake !")
    global treats_per_day
    with open('treat-count.txt') as f:
        lines = f.read().splitlines()
        for l in lines:
            splt = l.split( ' ' )
            if len(splt) == 2:
                try:
                    treats_per_day[splt[0]] = int(splt[1])
                except ValueError:
                    treats_per_day[splt[0]] = 0
    global pic_links
    with open('pic-links.txt') as f:
        pic_links = f.read().splitlines()


@bot.command()
async def nerd( ctx ):
    await ctx.send( f"https://discordapp.com/channels/851934793817129010/851934794262773762/928391917287403600" )    

bot.run(open('token.txt').read())
