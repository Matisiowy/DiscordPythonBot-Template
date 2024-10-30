import discord

name = "ping"

async def run(message, voice_clients,):
    try:
      await  message.channel.send("Pong!")
    except Exception as e:
        print(e)