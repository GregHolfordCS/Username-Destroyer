import discord
from discord.ext import commands
import random

description = '''Fun bot to mess with friends who steal my nickname in discord'''
bot = commands.Bot(command_prefix='~', description=description)

print('Loading and reading config file')
configFile = open("config.txt", "r", encoding='utf-8')
#TODO: This is a lazy way of writing a config but it encrypts details that should not be uploaded to git.
for line in configFile:
    strSplit = line.split(": ")
    attribute = strSplit[1].replace('\n', '')
    if "Token" in line:
        token = attribute
        print(f'Token: {token}')
    elif "Owner" in line:
        owner = attribute
        ownerID = owner.split("#")[1]
        print(f'Owner: {owner}')
    elif "Replace" in line:
        replaceName = attribute
        print(f'Replace Name: {replaceName}')
configFile.close()


DEBUG = False

print(f'DEBUG: {DEBUG}')
print('------')
print('')
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context = True)
async def hi(ctx):
    await bot.say('hi')

#Debug method to set everyones nicks to the owners.
#We really don't want this method to be available for use unless absolutely nescessary
@bot.command(pass_context = True)
async def setnicks(ctx):
    if DEBUG:
        author = str(ctx.message.author)
        print(f'Author: {author}')
        if author != owner:
            await bot.say("Nah dude")
        else:
            for member in bot.get_all_members():
                if not str(member) == "UsernameDestroyer#1056":
                    await bot.say(f'{str(member)} -> {owner}')
                    try:
                        await bot.change_nickname(member, owner)
                    except:
                        await bot.say(f'No perms to set nickname for: {str(member)}')
    else:
        await bot.say(f'Debug mode is {DEBUG}. This is not allowed bro.')



@bot.command(pass_context = True)
async def destroyidiots(ctx, name : str):
    author = str(ctx.message.author)
    print(f'Author: {author}')
    if author != owner:
        await bot.say("Nah dude")
    else:
        hasObliterated = False;
        for member in bot.get_all_members():
            username = str(member).split("#")[0]
            id = str(member).split("#")[1]
            nick = member.nick
            if nick is None:
                nick = username
            if nick == name and id != ownerID:
                hasObliterated = True
                try:
                    await bot.change_nickname(member, replaceName)
                    await bot.say("Obliterating: " + username + "#" + id + f' -> {replaceName}#' + id)
                except:
                    await bot.say(f'No perms to set nickname for: {str(member)}')
                print("Obliterating: " + name + "#" + id)
            #await bot.say(f'Arg: {name} Member: {str(member)} Nick: {member.nick} UsernameSplit: {username} ID Split: {id}')
            print(f'Arg: {name} Member: {str(member)} Nick: {member.nick} UsernameSplit: {username} ID Split: {id}')
        if not hasObliterated:
            await bot.say(f'Nobody found to destroy this time with the nick: {name}')
        print("Finished command")

@bot.command(pass_context = True)
async def destroyidiotssubstr(ctx, name : str):
    author = str(ctx.message.author)
    print(f'Author: {author}')
    if author != owner:
        await bot.say("Nah dude")
    else:
        hasObliterated = False;
        for member in bot.get_all_members():
            username = str(member).split("#")[0]
            id = str(member).split("#")[1]
            nick = member.nick
            if nick is None:
                nick = username
            if name in nick and id != ownerID:
                hasObliterated = True
                try:
                    await bot.change_nickname(member, "DestroyedIdiot")
                    await bot.say("Obliterating: " + username + "#" + id + f' -> {replaceName}#' + id)
                except:
                    await bot.say(f'No perms to set nickname for: {str(member)}')
                print("Obliterating: " + name + "#" + id)
            #await bot.say(f'Arg: {name} Member: {str(member)} Nick: {member.nick} UsernameSplit: {username} ID Split: {id}')
            print(f'Arg: {name} Member: {str(member)} Nick: {member.nick} UsernameSplit: {username} ID Split: {id}')
        if not hasObliterated:
            await bot.say(f'Nobody found to destroy this time with the nick: {name}')

bot.run(f'{token}')