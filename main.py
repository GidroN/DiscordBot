import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import Permissions
from youtubesearchpython import VideosSearch
import os
import requests
import asyncio
import json
import random
import pafy
import lyricsgenius

TOKEN = os.environ['TOKEN'] # NEED YOUR DISCORD TOKEN
GENIUS_TOKEN = os.environ['GENIUS_TOKEN'] # NEED YOUR GENIUS TOKEN
FFMPEG_PATH = r'' # path to your ffmpeg.exe (for example - C:\Program Files\FFMPEG\bin\ffmpeg.exe)
genius = lyricsgenius.Genius(GENIUS_TOKEN)
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_member_join(member: discord.Member):
    role = get(member.guild.roles, id=988491899553845269)
    await member.add_roles(role)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.reply("The command is not found.")
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.reply('Argument missing.')
    if isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.reply('Member not found.')
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.reply('Not enough permissions.')
    if isinstance(error, discord.ext.commands.errors.NotOwner):
        await ctx.reply('You are not owner of the bot.')
    if isinstance(error, discord.ext.commands.errors.BotMissingPermissions):
        await ctx.reply('Bot have not enough permissions for this command.')


@bot.command()
@commands.is_owner()
async def kick(ctx, member: discord.Member, reason=None):
    """
    :description: You can kick somebody.
    :param member: @MEMBER - with mention
    :example: .kick @MEMBER
    :param reason: some reason
    :return: kick somebody
    """
    await member.kick(reason=reason)
    await asyncio.sleep(2)
    await ctx.channel.purge(limit=1)
    await ctx.send(f"{member} kicked. Reason: {reason}")


@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, reason=None):
    """
    :description: You can ban everything. Aahahah.
    :param member: @MEMBER - with mention
    :param reason: optional - reason.
    :return: BAN THIS FUCKING SHIT.
    """
    url = member.avatar_url
    embed = discord.Embed(color=0x000000, title=f'Goodbye for now.')
    embed.set_image(url=f'https://some-random-api.ml/canvas/wasted?avatar={str(url)[:str(url).rfind(".") + 1] + "png"}')
    await ctx.send(embed=embed)
    await asyncio.sleep(2.5)
    await member.ban(reason=reason)
    await asyncio.sleep(2)
    await ctx.channel.purge(limit=2)
    await ctx.send(f"{member} banned. Reason: {reason}")


@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, member: discord.Member, reason=None):
    """
    :description: I`m trying to make this shit working.
    :param member: @MEMBER - with mention
    :param reason: reason - optional.
    :return: Unban.
    """
    await member.unban(reason=reason)
    await ctx.send(f"{member} unbanned. Reason: {reason}")
    await asyncio.sleep(2)
    await ctx.channel.purge(limit=2)


@bot.command()
async def count_members(ctx):
    """
    :description: Nothing interesting.
    :return: integer. Count of the member.
    """
    members = ctx.message.guild.members
#     for member in members:
#         await ctx.send(f"Member found: {member.mention}")
    await ctx.reply(len(members))


@bot.command()
async def avatar(ctx, member: discord.Member):
    """
    :description: let you get the members avatar
    :param member: @MEMBER .Where @MEMBER - is a member with mention.
    :return: Link.
    """
    await ctx.reply(member.avatar_url)


@bot.command()
async def get_id(ctx, member: discord.Member):
    """
    :description: Get the id of member.
    :param member: write the member
    example: .get_id @MEMBER. Where @MEMBER - member with mention.
    :return: id
    """
    await ctx.reply(f"{member} id: {member.id}")


@bot.command()
async def get_member_by_id(ctx, id: int):
    """
    :description: Get the member by id.
    :param id: write id of the member.
    :example .get_member_by_id ID. Where ID - member id. You can get it by the command - get_id
    :return: member
    """
    await ctx.reply(f"This id has member: {ctx.guild.get_member(id).mention}")


@bot.command()
@commands.has_permissions(manage_channels=True)
async def clear(ctx, limit: int = 10):
    """
    IMPORTANT: ONLY MODER CAN USE THIS COMMAND.
    description: Let your clear the messages.
    :param limit: write how many message do you wanna clear.
    :example .clear 10
    :return: clears the messages
    """
    await ctx.channel.purge(limit=limit + 1)
    await ctx.channel.send('Wait a moment, the messages are deleting...')
    await asyncio.sleep(0.8)
    await ctx.channel.purge(limit=1)


@bot.command()
async def spam_text(ctx, text: str = 'spam', limit: int = 10):
    """
    :description: Let to spam with text
    :param text: text
    :param limit: how much spams.
    :return: spams
    """
    await ctx.channel.purge(limit=1)
    for i in range(limit + 1):
        await asyncio.sleep(0.5)
        await ctx.send(text)


@bot.command()
async def image(ctx: discord.Message):
    """
    :description: let you show a random image. Default - random image
    :param ctx: just your message after the command Otherwise you will fucked up)
    :example: .image cat | .image meme - new feature.
    :return: random animal image
    """
    animals = ['cat', 'dog', 'fox', 'bird', 'koala', 'raccoon', 'kangaroo', 'red_panda', 'whale', 'birb']
    if len(ctx.message.content) <= 7:
        content = random.choice(animals)
    else:
        content = ctx.message.content[7:]
        content = content.lower()

    if content in animals:
        response = requests.get(f'https://some-random-api.ml/animal/{content}')
    if content == 'meme':
        response = requests.get('https://some-random-api.ml/meme')
    try:
        json_data = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        await ctx.reply("YOU FUCKED UP!")
    else:
        embed = discord.Embed(color=0xff9900, title=f'Random {content}')
        embed.set_image(url=json_data['image'])
        await ctx.reply(embed=embed)


@bot.command()
async def hug(ctx, member: discord.Member):
    """
    :description: You can hug somebody.
    :param member: @MEMBER. Where @MEMBER - member with mention.
    :example: .hug @MEMBER
    :return: hug gif
    """
    response = requests.get('https://some-random-api.ml/animu/hug')
    json_data = json.loads(response.text)
    embed = discord.Embed(color=0xff9900, title=f"{member.name} it's for you.")
    embed.set_image(url=json_data['link'])
    await ctx.reply(embed=embed)


@bot.command()
async def pat(ctx, member: discord.Member):
    """
    :description: You can pat somebody.
    :param member: @MEMBER. Where @MEMBER - member with mention.
    :example: .pat @MEMBER
    :return: pat gif
    """
    response = requests.get('https://some-random-api.ml/animu/pat')
    json_data = json.loads(response.text)
    embed = discord.Embed(color=0xff9900, title=f"{member.name} it's for you.")
    embed.set_image(url=json_data['link'])
    await ctx.reply(embed=embed)


@bot.command()
async def lyrics(ctx, *, args):
    """
    :param name of the song:
    :example: '21 pilots stressed out'
    :return: lyrics
    """
    song = genius.search_song(title=args)
    if song is None:
        await ctx.reply("No songs found.")
        print("-" * 80)
        return

    embed = discord.Embed(color=0xff9900, title=f"Lyrics for {song.title} - {song.artist}",
                          description=f'{song.lyrics}')
    embed.set_image(url=song.song_art_image_url)
    print("-" * 80)
    await ctx.reply(embed=embed)


@bot.command(name='connect', help='This command connects the bot.')
async def connect(ctx):
    """
    :description: let bot connect to your voice channel
    """
    if not ctx.message.author.voice:
        await ctx.reply(f"{ctx.author.name} is not connected to a voice channel")
        return
    else:
        channel = ctx.author.voice.channel
    try:
        await channel.connect()
    except discord.errors.ClientException:
        await ctx.reply('The bot is already connected.')


@bot.command(name='disconnect', help='This command disconnects the bot.')
async def disconnect(ctx):
    """
    :description: let bot disconnect from your voice channel
    """
    voice_client = ctx.message.guild.voice_client
    if voice_client is not None:
        if voice_client.is_connected():
            await voice_client.disconnect()
    else:
        await ctx.reply("The bot is not connected to a voice channel.")


@bot.command(name='stop', help='This commands stops the song.')
async def stop(ctx):
    """
    :description: stop the bot playing music
    """
    voice_client = ctx.message.guild.voice_client
    if voice_client is not None:
        if voice_client.is_connected() and voice_client.is_playing():
            voice_client.stop()
    else:
        await ctx.reply('The bot is not connected or is not playing.')


@bot.command(name='pause', help='This command pauses the song.')
async def pause(ctx):
    """
    :description: pauses the music
    """
    voice_client = ctx.message.guild.voice_client
    if voice_client is not None:
        if voice_client.is_playing():
            voice_client.pause()
    else:
        await ctx.reply("The bot is not playing anything at the moment.")


@bot.command(name='resume', help='This command resumes the song.')
async def resume(ctx):
    """
    :description: resumes the music
    """
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client is not None:
        if voice_client.is_paused():
            voice_client.resume()
    else:
        await ctx.reply("The bot was not playing anything before this. Use play command")


@bot.command()
async def play(ctx, *, url):
    """
    :description: Let the bot play music.
    :param url: url or a search query
    :return: MUSICA.
    """
    if ctx.message.author.voice is None:
        await ctx.reply(f"No Voice Channel {ctx.author} you need to be in a voice channel to use this command!")
        return

    voice_client = ctx.message.guild.voice_client
    if voice_client is not None:
        if voice_client.is_playing():
            await ctx.reply('A song is already playing. At the moment I have no queue. Sorry =(.')
            return

    if not url.startswith('https://'):
        videosSearch = VideosSearch(url, limit=1)
        result = videosSearch.result()
        url = result['result'][0]['link']
        name = result['result'][0]['title']
        preview = result['result'][0]['thumbnails'][0]['url']
        duration = result['result'][0]['duration']

        embed = discord.Embed(color=0xff9900, title=f"Playing {name}")
        embed.set_image(url=preview)
        embed.add_field(name='link', value=url, inline=False)
        embed.add_field(name='duration', value=duration, inline=True)
        await ctx.reply(embed=embed)

    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client is None:
        voice_client = await voice.connect()
    else:
        await voice_client.move_to(channel)

    song = pafy.new(url)  # creates a new pafy object
    audio = song.getbestaudio()  # gets an audio source
    source = FFmpegPCMAudio(executable=FFMPEG_PATH, source=audio.url, **FFMPEG_OPTIONS)   # converts the youtube audio source into a source discord can use
    voice_client.play(source)  # play the source


@bot.command()
@commands.has_permissions(administrator=True)
async def moder(ctx, member: discord.Member):
    role = discord.utils.find(lambda r: r.name == 'moder', ctx.message.guild.roles)
    if role in member.roles:
        await ctx.send("The member already has this role.")
        await asyncio.sleep(1)
        await ctx.channel.purge(limit=2)
    else:
        await member.add_roles(role)
        await ctx.send(f"The role moderator was give to {member.mention}")
        await asyncio.sleep(1)
    await ctx.channel.purge(limit=2)


@bot.command()
@commands.has_permissions(administrator=True)
async def remove_moder(ctx, member: discord.Member):
    role = discord.utils.find(lambda r: r.name == 'moder', ctx.message.guild.roles)
    if role in member.roles:
        await member.remove_roles(role)
        await ctx.send(f"The role moderator was removed, {member.mention}")
        await asyncio.sleep(1)
        await ctx.channel.purge(limit=2)
    else:
        await ctx.send("The member hasn't this role.")
        await asyncio.sleep(1)
    await ctx.channel.purge(limit=2)


@bot.event
async def on_message(message):
    if message.content.startswith('.hello'):
        await message.channel.send(message.content[7:])

    await bot.process_commands(message)


bot.run(TOKEN)
