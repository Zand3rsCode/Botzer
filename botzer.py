import asyncio
import discord
import random
from discord.ext.commands import Bot
import os


BOT_PREFIX = ("!")


TOKEN = open("/home/pi/botzer/token.txt","r").readline()

client = Bot(command_prefix=BOT_PREFIX)

folder=os.path.dirname(os.path.realpath(__file__)) 
def get_channel_list():
	channelfile = open(os.path.join(folder,'channellist.txt'),"r")
	imageonlychannels = channelfile.read().splitlines()
	channelfile.close()
	return imageonlychannels
imageonlylist = get_channel_list()

@client.event
async def on_ready():

	print(f'Logged in as {client.user}')


####################### LOTTO START ##############################

@client.command()
async def botzer(ctx):
    embed=discord.Embed(title="hjälp Kommandon", description="Bottens alla kommandon.", color=0xeff542)
    embed.add_field(name="Lotto hjälp", value="!lottohelp", inline=False)
    embed.add_field(name="Slå på och av bildlås i kanal", value="!imonly", inline=False)
    embed.set_thumbnail(url= "https://livgardet.se/images/lotto-loggan.png")
    await ctx.send(embed=embed)

@client.command()
async def lottohelp(ctx):
    embed=discord.Embed(title="Lotto Kommandon", description="Välj kommando följt av antal deltagare, tex !lotto 500", color=0xeff542)
    embed.add_field(name="En Vinnare", value="!lotto", inline=False)
    embed.add_field(name="Tre Vinnare", value="!lotto3", inline=False)
    embed.add_field(name="Fem Vinnare", value="!lotto5", inline=False)
    embed.set_thumbnail(url= "https://livgardet.se/images/lotto-loggan.png")
    await ctx.send(embed=embed)

@client.command()
async def lotto(ctx, num):
    embed = discord.Embed(title="Livgardets Lotteri", color=0xeff542)
    try:
        arg = random.randint(1, int(num)) 
        embed.add_field(name="Vinnare", value=(arg), inline=True)
        embed.set_thumbnail(url= "http://livgardet.se/images/lotto-loggan.png")
    except ValueError:
        return await ctx.send("Endast hela nummer")
    else:
        return await ctx.send(embed=embed)

@client.command()
async def lotto3(ctx, num):
    embed = discord.Embed(title="Livgardets Lotteri", color=0xeff542)
    try:
        arg1 = random.randint(1, int(num)) 
        embed.add_field(name="Vinnare 1", value=(arg1), inline=False)
        arg2 = random.randint(1, int(num)) 
        embed.add_field(name="Vinnare 2", value=(arg2), inline=False)
        arg3 = random.randint(1, int(num)) 
        embed.add_field(name="Vinnare 3", value=(arg3), inline=False)
        embed.set_thumbnail(url= "http://livgardet.se/images/lotto-loggan.png")
    except ValueError:
        return await ctx.send("Endast hela nummer")
    else:
        return await ctx.send(embed=embed)

@client.command()
async def lotto5(ctx, num):
    embed = discord.Embed(title="Livgardets Lotteri", color=0xeff542)
    try:
        arg1 = random.randint(1, int(num)) 
        embed.add_field(name="Vinnare 1", value=(arg1), inline=False)
        arg2 = random.randint(1, int(num)) 
        embed.add_field(name="Vinnare 2", value=(arg2), inline=False)
        arg3 = random.randint(1, int(num)) 
        embed.add_field(name="Vinnare 3", value=(arg3), inline=False)
        arg4 = random.randint(1, int(num)) 
        embed.add_field(name="Vinnare 4", value=(arg4), inline=False)
        arg5 = random.randint(1, int(num)) 
        embed.add_field(name="Vinnare 5", value=(arg5), inline=False)
        embed.set_thumbnail(url= "http://livgardet.se/images/lotto-loggan.png")
    except ValueError:
        return await ctx.send("Endast hela nummer")
    else:
        return await ctx.send(embed=embed)

####################### END OF LOTTO #########################

@client.command('imageonly')
async def imageonly(message):
	channel = message.channel
	global imageonlylist
	if(imageonlylist):
		if(str(channel.id) in imageonlylist):
			def checkauthor(m2):
				return message.author ==m2.author
			await channel.send("Image only mode disabled")
			tempchannellist=get_channel_list()
			tempchannellist.remove(str(channel.id))
			channelfile=open("channellist.txt", "w")
			if(len(tempchannellist)==0):
				pass
			else:
				channelfile.writelines(["%s\n" % item  for item in tempchannellist])
			channelfile.close()
			imageonlylist=tempchannellist
			print(imageonlylist)
		else:
			def checkauthor(m2):
				return message.author ==m2.author
			await channel.send("Image only mode enabled")
			channelid = channel.id
			imageonlylist.append(str(channel.id))
			print(imageonlylist)
			channelfile = open("channellist.txt","w")
			channelfile.writelines(["%s\n" % channelid])
			channelfile.close()
			await message.message.delete()

	#repeated code for lower level if statement
	else:
		def checkauthor(m2):
			return message.author ==m2.author
		await channel.send("Image only mode enabled")
		channelid = channel.id
		imageonlylist.append(str(channel.id))
		channelfile = open("channellist.txt","w")
		channelfile.writelines(["%s\n" % item  for item in imageonlylist])
		channelfile.close()
		await message.message.delete()

		#channelfile = open("channellist.txt","w+")
		#await client.get_channel(imageonlychannels[0]).send("testing saving")

@client.event
async def on_message(message):
    await client.process_commands(message)
    channel = message.channel
    global imageonlylist
    if (not message.author.bot):
        if(str(channel.id) in imageonlylist and message.author != client.user):
            if (message.attachments):
                pass
            elif(len(message.content) > 0):
                if(message.content[0:8] == 'https://'):
                    pass
                else:
                    try:
                        await message.delete()
                        await message.author.send('Tjenixen, Du får detta meddelande eftersom du har skrivit i kanalen #Dps-Test. Vi har gjort så för att förhindra spam i kanalen. Vänligen använd <#701505046080389180> istället!')
                    except discord.errors.NotFound:
                        pass
                    else:
                        try:
                            await message.delete()
                            await message.author.send('Tjenixen, Du får detta meddelande eftersom du har skrivit i kanalen #Dps-Test. Vi har gjort så för att förhindra spam i kanalen. Vänligen använd <#701505046080389180> istället!')
                        except discord.errors.NotFound:
                            pass


async def list_servers():
	await client.wait_until_ready()
	while not client.is_closed:
		print("Current servers:")
		for server in client.servers:
			print(server.name)
		await asyncio.sleep(600)

try:
	client.loop.create_task(list_servers())
	client.run(TOKEN)
except:
	channelfile = open("channellist.txt","w")
	channelfile.writelines(["%s\n" % item  for item in imageonlylist])
	channelfile.close()
