# 391669344695877632

import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import sqlite3
from ai_actions import*

######ALL CODE BELOW IS FOR INIT######
# Load .env
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Intents
intents = discord.Intents.default()
intents.message_content = True  # Required for ! commands

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        guild = discord.Object(id=391669344695877632)  # <-- Replace with your Guild ID!

        # Sync slash commands to this GUILD for instant update
        await self.tree.sync(guild=guild)
        print(f"Synced slash commands to test guild {guild.id}")

        # Also push changes globally — so they update for all servers
        await self.tree.sync()
        print(f"Synced slash commands globally too (may take up to 1 hour to appear globally)")

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

bot = MyBot()

conn = sqlite3.connect("bot_data.db")
cursor = conn.cursor()

######ALL CODE BELOW IS SQL######
cursor.execute("""
CREATE TABLE IF NOT EXISTS voice_persona (
    user_id TEXT PRIMARY KEY,
    instructions TEXT)               
""")

conn.commit

######ALL CODE BELOW IS FOR COMMANDS######
@bot.tree.command(name="ai", description="Sends a prompt to Chat GPT")
@app_commands.describe(message="Enter your prompt ")
async def ai_text(interaction: discord.Interaction, message: str):
    await handle_ai_text(message, interaction.response.send_message)

@bot.tree.command(name="text_to_speech", description="Converts text to speech with a random voice.")
@app_commands.describe(message="Enter your text to be converted ")
async def ai_tts(interaction: discord.Interaction, message: str):
    await handle_ai_tts(message, interaction.response.send_message)

@bot.tree.command(name="voice", description="Changes the instructions for text to speech")
@app_commands.describe(message="Enter your voice instructions")
async def ai_voice(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("Voice instructions updated!", ephemeral=True)


"""Examples
# Example ! prefix command
@bot.command()
async def ping(ctx):
    await ctx.send("Pong! (prefix)")

# Example / slash command
@bot.tree.command(name="ping", description="Replies with Pong! (slash)")
async def slash_ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! (slash)")
"""

bot.run(DISCORD_TOKEN)
