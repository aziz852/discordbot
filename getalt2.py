git push heroku master
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import string
import os
################CONFIGURE
discordCmdPrefix = "!"
cooldownSeconds = 30
cooldownAttempts = 1
altStorageFile = '/root/data/accounts.yml'
altRecieveLogChannelId = None
discordToken = None #Set to your Discord token in quotes.
accountMessage = "<@{0.message.author.id}> has recieved account: "
onCooldown = "This command is on cooldown for another `{0}` seconds."
sendAltMsg = "Here is your account: "
stockError = "Seems we are out of free accounts...check back later."
accRem = 1 #DO NOT EDIT UNLESS YOU USE A \n\n DELIMITER
gameNameDefault = "!getalt for alts"
stockCheckCommandEnabled = "true"
stockCheckOutputZone = "user" #This value can be "user", "channel", or "echannel". User is a direct message, channel is to the channel the message was from, ane echann$
stockCheckOutputeChannel = None #Set this to the channel ID in quotes of the output channel if the above value is "echannel"
stockCheckMessage = "Our current stock of accounts is: `{0}`"
setGameStock = "true" #Set to "true" if you wish to set the game name to the stock amount.
stockGameFormat = "Alt Stock: "
stockCooldownSeconds = 3
stockCooldownAttempts = 1
debug = "false"
################CONFIGURE
################SYSLANG#DO NOT TOUCH#
onReadyBegin = 'Logged in as '
onReadyId = ' with the user ID of '
parser = "`"
true = "true"
stockZeroWarn = "Out of Accounts"
user = "user"
channel = "channel"
echannel = "echannel"
configWarn = "Invalid Configuration!"
invalidToken = "Invalid Discord Token!"
################SYSLANG#DO NOT TOUCH#
client = commands.Bot(command_prefix=discordCmdPrefix)
@client.event
async def on_ready():
    print(onReadyBegin + client.user.name + onReadyId + client.user.id)
    await client.change_presence(game=discord.Game(name=gameNameDefault))
@client.command(pass_context = True)
@commands.cooldown(cooldownAttempts, cooldownSeconds, commands.BucketType.user)
async def getalt(ctx):
    if not os.stat(altStorageFile).st_size == 0:
        with open(altStorageFile, 'r') as f:
                sendAlt = f.readline()
                sendMessage = sendAltMsg + parser + sendAlt + parser
                with open(altStorageFile, 'r') as r:
                    r.next()
                    data = ""
                    for line in r:
                        data = data + line
                with open(altStorageFile, 'w') as w:
                    w.write(data)
                await client.send_message(ctx.message.author, sendMessage)
                await client.delete_message(ctx.message)
                if altRecieveLogChannelId is not None:
                    accountMessageSend = accountMessage + parser + sendalt + parser
                    await client.send_message(client.get_channel(altRecieveLogChannelId), accountMessageSend.format(ctx))
                if setGameStock == true:
                    with open(altStorageFile) as w:
                        stock = len(w.readlines())
                        stockgame = stockGameFormat + stock
                        await client.change_presence(game=discord.Game(name=stockgame))
    else:
        print(stockZeroWarn)
        await client.send_message(ctx.message.author, stockError)
@client.command(pass_context = True)
@commands.cooldown(stockCooldownAttempts, stockCooldownSeconds, commands.BucketType.user)
async def stock(ctx):
    if stockCheckCommandEnabled == true:
        with open(altStorageFile) as w:
            stock = len(w.readlines())
            stockCheckFormat = stockCheckMessage.format(stock)
            if stockCheckOutputZone == user:
                await client.send_message(ctx.message.author, stockCheckFormat.format(ctx))
            elif stockCheckOutputZone == channel:
                await client.send_message(ctx.message.channel, stockCheckFormat.format(ctx))
            elif stockCheckOutputZone == echannel and stockCheckOutputeChannel is not None:
                await client.send_message(client.get_channel(stockCheckOutputeChannel), accountMessageSend.format(ctx))
            else:
                print(configWarn)
    await client.delete_message(ctx.message)
@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await client.send_message(ctx.message.author, onCooldown.format(error.retry_after))
        await client.delete_message(ctx.message)
    if debug == true:
        raise error
if discordToken is not None:
    client.run(discordToken)
else:
    print(invalidToken)
