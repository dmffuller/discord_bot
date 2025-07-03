import discord
import os
from dotenv import load_dotenv
import sqlite3
from ai_actions import*

# Grab the API Token from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
client = OpenAI(api_key=OPENAI_TOKEN)
                
# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Required for on_message

# Pass intents to Client
bot = discord.Client(intents=intents)

# Create Var
log = []

#Setup SQLite
conn = sqlite3.connect("message_log.db")
cursor = conn.cursor()


# Responds to Hello message
async def hello_response(message):
    """Says a nice message"""
    await message.channel.send("Hey loser")

# Log User Messages
async def log_message(message):
    """Logs all user messages"""
    if message.content.upper() == "!YAP" or message.content.upper().startswith("!AI"): # do not log if user is bot commands
        return

    cursor.execute("""
        INSERT INTO messages (author, server, channel, content, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        f"{message.author.name}#{message.author.discriminator}",
        message.guild.name,
        message.channel.name if hasattr(message.channel, 'name') else str(message.channel),
        message.content,
        str(message.created_at)
    ))
    conn.commit()

# Yap Checker
async def yap_check():
    """Checks who is talking the most"""
    server_name = "VR Chat Losers"
    
    cursor.execute("""
    SELECT
        author,
        COUNT(*) AS message_count
    FROM
        messages
    WHERE
        Date(timestamp) = DATE('now')
        AND server = ?
    GROUP BY
        author
    ORDER BY
        message_count DESC
    LIMIT 1
    """, (server_name,))

    row = cursor.fetchone()
    if row:
        print(f"Top yapper for today: {row[0]} with {row[1]} messages.")    
    else:
        print("No messages yet today")


# On Ready Event
@bot.event
async def on_ready():
    guild_count = 0

    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count += 1

    print("VR Chat Bot is in " + str(guild_count) + " guilds(servers).")

    cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT,
    server TEXT,
    channel TEXT,
    content TEXT,
    timestamp TEXT
)
""")
conn.commit()

# On Message Event Loop
@bot.event
async def on_message(message):
    if message.author == bot.user: # No action if message is from bot
        return
    
    if message.content.upper() == "HELLO": # Hello response
        await hello_response(message)
    elif message.content.upper().startswith("!AI"): # AI Handeler
        await handle_ai_text(message)
    elif message.content.upper().startswith("!IMAGE"): # AI Handeler
        await handle_ai_image(message)
    elif message.content.upper().startswith("!TTS"): # AI Handeler
        await handle_ai_tts(message)
    elif message.content.upper().startswith("!VOICE"): # AI Handeler
        await change_instructions(message)
    elif message.content.upper().startswith("!YAP"): # Checks who sent the most words
        await yap_check()

    await log_message(message) # Message Logger
    cursor.execute("SELECT * FROM messages ORDER BY id DESC LIMIT 5") # This is printing the entire log, can delete, this is for testing
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Executes bot with public token
bot.run(DISCORD_TOKEN)