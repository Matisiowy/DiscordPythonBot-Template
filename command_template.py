import discord

name = "name_of_your_command"

async def run(message, voice_clients,):
    try:
        await message.channel.send("")
    except Exception as e:
        print(e)