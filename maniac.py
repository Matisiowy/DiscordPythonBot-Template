import discord
import os
import importlib
from datetime import datetime, timedelta
from pytz import timezone
from dotenv import load_dotenv


def run_bot():
    load_dotenv()
    TOKEN = os.getenv('discord_token')
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    client = discord.Client(intents=intents)

    commands_dict = {}


    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"@Your_name! || Version:{os.getenv('version')}"))
        print(f"[{datetime.now(timezone('Europe/Warsaw')).strftime('%H:%M')}]: Project has succesfully logged to discord as {client.user}.")
        load_commands()

    def load_commands():
        commands_dir = "./commands"
        if not os.path.exists(commands_dir):
            print(f"[{datetime.now(timezone('Europe/Warsaw')).strftime('%H:%M')}]: 📁 Cannot find directory 'commands'.")
            return

        files = [f for f in os.listdir(commands_dir) if f.endswith('.py')]
        if len(files) == 0:
            print(f"[{datetime.now(timezone('Europe/Warsaw')).strftime('%H:%M')}]: 📁 There is no files in 'commands'.")
            return

        for file in files:
            try:
                module_name = file[:-3]
                module = importlib.import_module(f'commands.{module_name}')
                if hasattr(module, 'name') and hasattr(module, 'run'):
                    commands_dict[module.name] = module.run
                    print(f"[{datetime.now(timezone('Europe/Warsaw')).strftime('%H:%M')}]: ✅ Loaded command: {module.name}")
                else:
                    print(f"[{datetime.now(timezone('Europe/Warsaw')).strftime('%H:%M')}]: ⚠️ File: {file} don't have required parameters `name` and `run`")
            except Exception as e:
                print(f"[{datetime.now(timezone('Europe/Warsaw')).strftime('%H:%M')}]: ❌ Can't load {file}: {e}")


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return


        if message.content.startswith("!"):
            command, *args = message.content[1:].split()
            if command in commands_dict:
                await commands_dict[command](message, client)

    client.run(TOKEN)

if __name__ == "__main__":
    run_bot()
