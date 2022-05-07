from threading import Lock
import discord
from discord.ext import commands
import random
from datetime import date

description = '''Tony bot commands'''

class PicLink:
    def __init__(self, seen, addr):
        self.seen = seen
        self.addr = addr

class PicLinks:
    def __init__( self ):
        self.pic_links = []
        self.lock = Lock()
        self.load_pic_links()

    def load_pic_links( self ):
        with self.lock:
            with open( 'pic-links.txt' ) as f:
                for line in f.read().splitlines():
                    splt = line.split( ' ' ) # Line is [X|O] link
                    if len( splt ) == 1:
                        self.pic_links.append(PicLink(False, splt[0]))
                    elif len( splt ) > 1:
                        self.pic_links.append(PicLink(False if splt[0] == 'X' else True, splt[1]))
    
    def save_pic_links( self ):
        with self.lock:
            with open( 'pic-links.txt', 'w' ) as f:
                f.write( '\n'.join( '{} {}'.format( "O" if pic.seen else "X", pic.addr ) for pic in self.pic_links ) )

    def add_pic( self, link ):
        with self.lock:
            self.pic_links.append( PicLink( False, link ) )
        self.save_pic_links()

    def get_pic( self ):
        found_addr = None
        with self.lock:
            tries = 0
            found_pic = None

            # pic a random picture
            while tries < 1000:
                pic = random.choice( self.pic_links )
                if not pic.seen:
                    found_pic = pic
                    break
                tries = tries + 1

            # Didn't find a pic
            if not found_pic:
                for pic in self.pic_links:
                    pic.seen = False
                found_pic = random.choice( self.pic_links )
            
            found_pic.seen = True
            found_addr = found_pic.addr
        self.save_pic_links()
        return found_addr

    def remove_pic( self, link ):
        deleted = False
        with self.lock:
            for i, pic in enumerate( self.pic_links ):
                if pic.addr == link:
                    self.pic_links.pop(i)
                    deleted = True
                    break
        if deleted:
            self.save_pic_links()
        return deleted

class TreatCounter:
    def __init__( self ):
        self.treat_count = {}
        self.lock = Lock()
        self.load_treat_counts();
    
    def load_treat_counts( self ):
        with self.lock:
            with open('treat-count.txt') as f:
                lines = f.read().splitlines()
                for l in lines:
                    splt = l.split( ' ' )
                    if len(splt) == 2:
                        try:
                            self.treat_count[splt[0]] = int(splt[1])
                        except ValueError:
                            self.treat_count[splt[0]] = 0
    
    def save_treat_counts( self ):
        with self.lock:
            with open( 'treat-count.txt', 'w' ) as f:
                for k, v in self.treat_count.items():
                    f.write( f'{k} {v}\n' )

    def treat( self ):
        treat_count = 0
        with self.lock:
            today = date.today().strftime("%d/%m/%Y")
            if today not in self.treat_count:
                self.treat_count[today] = 0
            self.treat_count[today] += 1
            treat_count = self.treat_count[today]
        self.save_treat_counts()
        return treat_count

    def vomit( self ):
        treat_count = 0
        treats_to_vomit = 0
        with self.lock:
            today = date.today().strftime("%d/%m/%Y")
            if today not in self.treat_count:
                self.treat_count[today] = 0
            treats_to_vomit = random.choice( range( 1, 5 ) )
            if self.treat_count[today] == 0:
                return 0, 0
            if self.treat_count[today] < treats_to_vomit:
                treats_to_vomit = self.treat_count[today]
            self.treat_count[today] -= treats_to_vomit
            if self.treat_count[today] < 0:
                self.treat_count[today] = 0
            treat_count = self.treat_count[today]
        self.save_treat_counts()
        return treats_to_vomit, treat_count

class CustomCommand:
    def __init__( self, name, text ):
        self.name = name
        self.text = text

class CustomCommands:
    def __init__( self, bot: commands.Bot ):
        self.commands = {}
        self.lock = Lock()
        self.load_commands()


    def load_commands( self ):
        with self.lock:
            with open('commands.txt') as f:
                lines = f.read().splitlines()
                for l in lines:
                    splt = l.split( ' ' )
                    if len(splt) >= 2:
                        name = splt[0]
                        text = splt[1]
                        command = CustomCommand( name, text )
                        self.commands.append( command )
    
    def save_commands( self ):
        with self.lock:
            with open('commands.txt', 'w') as f:
                for command in self.commands:
                    f.write( f'{command.name} {command.text}\n' )

    def register_command( self, bot, name, text ):
        with self.lock:
            command = CustomCommand( name, text )
            self.commands.append( command )

class App:
    def __init__( self ):
        self.pic_links = PicLinks()
        self.treat_count = TreatCounter()
        self.custom_commands = None




intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', description=description, intents=intents,  )
app = App()

@bot.command()
async def registercommand( ctx, name, text ):
    global app
    global bot
    app.custom_commands.register_command( bot, name, text )
    await ctx.send("Command registered")

@bot.command()
async def meow( ctx ):
    emote = random.choice( ["<:tonyaah:860900789925183518>", "<:tonyhappy:860900538317406218>"])
    await ctx.send( emote + ' meow ' + emote )

@bot.command()
async def moew( ctx ):
    emote = random.choice( ["<:tonyaah:860900789925183518>", "<:tonyhappy:860900538317406218>"])
    await ctx.send( emote + ' moew ' + emote )

async def sendpic( ctx ):
    global app
    addr = app.pic_links.get_pic()
    await ctx.send(addr)

@bot.command()
async def tonypic( ctx ):
    await sendpic( ctx )

@bot.command()
async def tounoirpic( ctx ):
    await sendpic( ctx )

@bot.command()
async def obiwan( ctx ):
    await ctx.send( f"<:tonyhappy:860900538317406218> le trailer d'obiwan: https://www.youtube.com/watch?v=EnlOhdFZSXw <:tonyhappy:860900538317406218>\n<:tonyhappy:860900538317406218><:tonyhappy:860900538317406218><:tonyhappy:860900538317406218><:tonyhappy:860900538317406218><:tonyhappy:860900538317406218><:tonyhappy:860900538317406218><:tonyhappy:860900538317406218>")

@bot.command()
async def treat( ctx ):
    global app
    total = app.treat_count.treat()
    await ctx.send( f"<:tonyhappy:860900538317406218> <:tonyhappy:860900538317406218> <:tonyhappy:860900538317406218> meow onm onm onm onm meow <:tonyhappy:860900538317406218> <:tonyhappy:860900538317406218> <:tonyhappy:860900538317406218>\n\t\t\t\tJ'en ai mangé {total} aujourd'hui.")

@bot.command()
async def vomit( ctx ):
    global app
    vomited, total = app.treat_count.vomit()
    if vomited == 0:
        await ctx.send( f"Je n'ai rien a vomir aujourd'hui <:tonysad:860900605383147551> Je suis affamé <:tonysad:860900605383147551>")    
    else:
        await ctx.send( f"🤮🤮🤮 blueaauearrrgg 🤮🤮🤮\n\t\t\tJ'ai vomis {vomited} treats\n\t\t\tJ'en ai mangé {total} aujourd'hui.")


@bot.command()
async def tonysleep( ctx ):
    await ctx.send( "<:zzzztony:890679784349265931><:zzzztony:890679784349265931> it is late meow, go to sleep <:zzzztony:890679784349265931><:zzzztony:890679784349265931>\n<:zzzztony:890679784349265931><:zzzztony:890679784349265931> it is late meow, go to sleep <:zzzztony:890679784349265931><:zzzztony:890679784349265931>\n<:zzzztony:890679784349265931><:zzzztony:890679784349265931> it is late meow, go to sleep <:zzzztony:890679784349265931><:zzzztony:890679784349265931>")

@bot.command()
async def addpic( ctx, link ):
    global app
    app.pic_links.add_pic( link )
    await ctx.send("J'ai ajouté cette image dans ma mémoire <:tonyhappy:860900538317406218>")

@bot.command()
async def removepic( ctx, link ):
    global app
    deleted = app.pic_links.remove_pic( link )
    if deleted:
        await ctx.send("J'ai enlevé l'image de ma mémoire <:tonyhappy:860900538317406218>")
    else:
        await ctx.send("Je n'ai pas cette image dans ma mémoire <:tonysad:860900605383147551>")


@bot.event
async def on_disconnect():
    print( "Meow! Going to sleep..." )

@bot.event
async def on_ready():
    print("Meow! I'm awake !")


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
