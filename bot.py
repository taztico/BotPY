import discord
import json
import aiohttp
import random
from discord.ext import commands
intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='>',intents=intents)

@bot.event
async def on_ready():
    game = discord.Game('Chupando Poto a lo desquiciao')
    await bot.change_presence(status=discord.Status.idle, activity=game)
    print('My Ready is Body')


@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.send(f"You have been banned in {ctx.guild} for {reason}")
    await member.ban(reason = reason)
    await ctx.send(f"{member} has been successfully banned.")
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=limit)

@bot.command(pass_context=True)
async def giphy(ctx, *, search):
    embed = discord.Embed(colour=discord.Colour.blue())
    session = aiohttp.ClientSession()

    if search == '':
        response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=IwFfaW58SavoJQe36VYUX1BZEsRDkY1V')
        data = json.loads(await response.text())
        embed.set_image(url=data['data']['images']['original']['url'])
    else:
        search.replace(' ', '+')
        response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=IwFfaW58SavoJQe36VYUX1BZEsRDkY1V&limit=10')
        data = json.loads(await response.text())
        gif_choice = random.randint(0, 9)
        embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

    await session.close()

    await ctx.send(embed=embed)

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(help="Prints details of Server")
async def where_am_i(ctx, limit : int):
    owner = str(ctx.guild.owner)
    region = str(ctx.guild.region)
    guild_id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    desc = ctx.guild.description

    embed = discord.Embed(
        title=ctx.guild.name + " Informacion del server :money_mouth:",
        description=desc,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Dueño", value=owner, inline=True)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Cantidad  de usuario", value=memberCount, inline=True)

    await ctx.send(embed=embed)

    memberCount1 = (ctx.guild.member_count)

    members = []
    if memberCount1<=10:
        async for member in ctx.guild.fetch_members(limit=limit):
            await ctx.send('Name : {}\t Status : {}\n Joined at {}'.format(member.display_name, str(member.status),
                                                                           str(member.joined_at)))
    else:
        await ctx.send("Son muchos usuarios amigo ><")
@bot.command()
async def tell_me(ctx):
    text = "Me llamo Cumgi y soy un sutro descarao creado por el Tazticock :smiling_imp:"
    await ctx.send(text)

@bot.command()
async def mierda(ctx):
    a = random.randint(0,100)
    if 0<a<20:
        text="eres solamente ",a," % mierda "
        await ctx.send(text)
    elif 20<a<40:
        text="eres ",a," % mierda "
        await ctx.send(text)
    elif 40<a<60:
        text="eres ",a," % mierda , punto medio usuario promedio"
        await ctx.send(text)
    elif 60<a<80:
        text="eres ",a," % mierda , casi como el @xelo"
        await ctx.send(text)
    elif 80<a<100:
        text="eres ",a," % mierda , eri como la mierda misma igual que el @xelo"
        await ctx.send(text)
@bot.command()
async def pastiter(ctx):
    await ctx.send("El pastero culiao ese")
@bot.command()
async def dex(ctx):
    await ctx.send("Waton culiao ese wuaja")

# A dictionary to keep track of user's balance
user_balance = {}

@bot.command()
async def slot(ctx, bet: float):
    # Check if user has enough balance to place the bet
    if ctx.author.id not in user_balance:
        await ctx.send("No teni AMIGODSRUT, usa !register para obtener una")
        return
    elif user_balance[ctx.author.id] < bet:
        await ctx.send("tai mas pobre pa hacer esta apuesta , tu saldo es {}".format(user_balance[ctx.author.id]))
        return
    # Deduct the bet from the user's balance
    user_balance[ctx.author.id] -= bet
    slot_options = [":smiling_imp:", ":nerd:", ":poop:", ":rainbow_flag:", ":bell:", ":moneybag:", ":seven:", ":peach:"]
    slot_result = [random.choice(slot_options) for i in range(3)]
    await ctx.send("Tiraste la palanca...\n{} | {} | {}".format(*slot_result))
    if slot_result[0] == slot_result[1] == slot_result[2]:
        # Jackpot prize
        prize = bet * 10
        user_balance[ctx.author.id] += prize
        await ctx.send("JACKPOT! Ganaste {}! Tu nuevo saldo es {}".format(prize, user_balance[ctx.author.id]))
    elif slot_result[0] == slot_result[1]:
        prize = bet * 2
        user_balance[ctx.author.id] += prize
        await ctx.send("Ganaste {}! Tu nuevo saldo es {}".format(prize, user_balance[ctx.author.id]))
    else:
        await ctx.send("Prueba de nuevo . Tu saldo es {}".format(user_balance[ctx.author.id]))

@bot.command()
async def register(ctx):
    # Create a balance for the user
    if ctx.author.id not in user_balance: 
        user_balance[ctx.author.id] = 100
        await ctx.send("Obtuviste una AMIGODSRUT , Tu saldo es {}".format(user_balance[ctx.author.id]))
    else:
        await ctx.send("Ya tienes una AMIGODSRUT , Tu saldo es {}".format(user_balance[ctx.author.id]))
@bot.command()
async def balance(ctx):
    if ctx.author.id not in user_balance:
        await ctx.send("No tiene una AMIGODSRUT , prueba con >register")
    else:
        await ctx.send("Tu saldo actual es {}".format(user_balance[ctx.author.id]))


bot.run('')
