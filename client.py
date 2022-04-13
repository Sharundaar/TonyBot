import discord
from discord.ext import commands
import random
from datetime import date

description = '''Tony bot commands'''

class Pic:
    def __init__( self, weight, addr ):
        self.weight = weight
        self.addr = addr

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', description=description, intents=intents )
pic_links = []
treats_per_day = {}

def load_pic_links():
    global pic_links
    with open('pic-links.txt') as f:
        for line in f.read().splitlines():
            splt = line.split(' ')
            if len( splt ) == 1:
                pic_links.append( Pic(0, splt[0] ) )
            else:
                pic_links.append( Pic(int(splt[0]), splt[1] ) )
    pic_links.sort( key=lambda x: x.weight )

def save_pic_links():
    global pic_links
    pic_links.sort( key=lambda x: x.weight )
    with open( 'pic-links.txt', 'w' ) as f:
        f.write( '\n'.join( '{} {}'.format( pic.weight, pic.addr ) for pic in pic_links ) ) 

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
    pic_links.sort( key=lambda x: x.weight )
    start = 0
    end = -1
    weight_target = pic_links[0].weight
    for i, lk in enumerate(pic_links):
        if lk.weight != weight_target:
            end = i
            break
    if end < 0:
        end = len( pic_links )
    pic = random.choice(pic_links[start:end])
    pic.weight = pic.weight + 1
    save_pic_links()
    await ctx.send(pic.addr)

@bot.command()
async def tounoirpic( ctx ):
    global pic_links
    pic_links.sort( key=lambda x: x.weight )
    start = 0
    end = -1
    weight_target = pic_links[0].weight
    for i, lk in enumerate(pic_links):
        if lk.weight != weight_target:
            end = i
            break
    if end < 0:
        end = len( pic_links )
    pic = random.choice(pic_links[start:end])
    pic.weight = pic.weight + 1
    save_pic_links()
    await ctx.send(pic.addr)

@bot.command()
async def obiwan( ctx ):
    await ctx.send( f"<:tonyhappy:860900538317406218> le trailer d'obiwan: https://www.youtube.com/watch?v=EnlOhdFZSXw <:tonyhappy:860900538317406218>\n<:tonyhappy:860900538317406218><:tonyhappy:860900538317406218><:tonyhappy:860900538317406218><:tonyhappy:860900538317406218><:tonyhappy:860900538317406218><:tonyhappy:860900538317406218><:tonyhappy:860900538317406218>")

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
async def vomit( ctx ):
    global treats_per_day
    today = date.today().strftime("%d/%m/%Y")
    if today not in treats_per_day:
        treats_per_day[today] = 0
    treats_to_vomit = random.choice( range( 1, 5 ) )
    if treats_per_day[today] == 0:
        await ctx.send( f"Je n'ai rien a vomir aujourd'hui <:tonysad:860900605383147551> Je suis affamé <:tonysad:860900605383147551>")    
        return
    if treats_per_day[today] < treats_to_vomit:
        treats_to_vomit = treats_per_day[today]
    treats_per_day[today] -= treats_to_vomit
    if treats_per_day[today] < 0:
        treats_per_day[today] = 0
    treat_count = treats_per_day[today]
    with open( 'treat-count.txt', 'w' ) as f:
        for k, v in treats_per_day.items():
            f.write( f'{k} {v}\n' )
    await ctx.send( f"🤮🤮🤮 blueaauearrrgg 🤮🤮🤮\n\t\t\tJ'ai vomis {treats_to_vomit} treats\n\t\t\tJ'en ai mangé {treat_count} aujourd'hui.")


@bot.command()
async def tonysleep( ctx ):
    await ctx.send( "<:zzzztony:890679784349265931><:zzzztony:890679784349265931> it is late meow, go to sleep <:zzzztony:890679784349265931><:zzzztony:890679784349265931>\n<:zzzztony:890679784349265931><:zzzztony:890679784349265931> it is late meow, go to sleep <:zzzztony:890679784349265931><:zzzztony:890679784349265931>\n<:zzzztony:890679784349265931><:zzzztony:890679784349265931> it is late meow, go to sleep <:zzzztony:890679784349265931><:zzzztony:890679784349265931>")

@bot.command()
async def addpic( ctx, link ):
    global pic_links
    pic_links.append( Pic( pic_links[0].weight, link ) )
    save_pic_links()
    await ctx.send("J'ai ajouté cette image dans ma mémoire <:tonyhappy:860900538317406218>")

@bot.command()
async def removepic( ctx, link ):
    global pic_links
    try:
        deleted = False
        for i, pic in enumerate( pic_links ):
            if pic.addr == link:
                pic_links.pop(i)
                deleted = True
                break
        if deleted:
            save_pic_links()
            await ctx.send("J'ai enlevé l'image de ma mémoire <:tonyhappy:860900538317406218>")
        else:
            await ctx.send("Je n'ai pas cette image dans ma mémoire <:tonysad:860900605383147551>")
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
    load_pic_links()


@bot.command()
async def nerd( ctx ):
    await ctx.send( f"https://tenor.com/view/the-simpsons-homer-simpson-nerd-yelling-insult-gif-7884166" )    

@bot.command()
async def bienjouer( ctx, person ):
    await ctx.send( f"Bien jouer champion <:tonyhappy:860900538317406218> Let's gooooooo " + person )

@bot.command()
async def promoL2( ctx ):
    msg = random.choice(["Vraiment tous des idiots <:tonycoler:903753147904847883>", "Des gros trou de balles <:tonycoler:903753147904847883>"])
    await ctx.send( msg )

@bot.command()
async def petitponey( ctx ):
    await ctx.send( 'https://www.youtube.com/watch?v=u5Ho1trvlro' )

@bot.command()
async def flute( ctx ):
    await ctx.send( 'https://discord.com/channels/851934793817129010/851934794262773762/951748893614407740' )

@bot.command()
async def jigglejiggle( ctx ):
    await ctx.send( 'https://www.youtube.com/watch?v=oreXlaA7p7g' )

bot.run(open('token.txt').read())
