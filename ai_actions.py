from openai import OpenAI
import os
from dotenv import load_dotenv
import discord
import io
import random

voice_bank = ["alloy", "ash", "ballad", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer", "verse"]
new_instructions="Speak very angrily and annoyed"

# Grab API Token
load_dotenv()
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
client = OpenAI(api_key=OPENAI_TOKEN)

# AI Prompt - Text
async def handle_ai_text(prompt: str, send_func):
    if prompt.strip() == "":
        await send_func("No prompt entered")
    else:
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"A discord user is giving you a prompt. Please keep responses under 3 sentences unless asked otherwise. Here is the prompt: {prompt}"}]
    )
        content = response.choices[0].message.content
        await send_func(content)

# AI Prompt - Image
async def handle_ai_image(message):
    prompt = message.content[6:].strip()
    if prompt == "":
        await message.channel.send("No prompt entered")
    else:
        response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        n=1,
        size="1024x1024",
        quality="low"
    )
        image_url = response.data[0].url
        await message.channel.send(image_url)

# AI Prompt - Audio
async def handle_ai_tts(prompt: str, send_func):
    if prompt == "":
        await send_func("No text entered")
    else:
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=random.choice(voice_bank),
            input=prompt,
            instructions=new_instructions
        )

        audio_data = response.content
        audio_file = discord.File(fp=io.BytesIO(audio_data), filename="speech.mp3")

        
        await send_func(file=audio_file)


# AI Instructions
async def change_instructions(prompt: str):
    """Changes the AI for how to speak"""
    global new_instructions
    new_instructions = prompt
    print("Voice Changed")

