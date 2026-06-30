import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import fal_client

load_dotenv()

DISCORD_TOKEN = os.getenv("discord_token")
FAL_KEY = os.getenv("FAL_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

fal_client.api_key = FAL_KEY


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def generate(ctx, *, prompt: str):
    await ctx.send(f"Generating image for: `{prompt}`...")

    try:
        result = await fal_client.run(
            "fal-ai/flux/dev",
            arguments={"prompt": prompt},
        )
        images = result.get("images", [])
        if images:
            embed = discord.Embed(title="Generated Image", description=prompt)
            embed.set_image(url=images[0].get("url", ""))
            await ctx.send(embed=embed)
        else:
            await ctx.send("No images were generated.")
    except Exception as e:
        await ctx.send(f"Error generating image: {e}")


@bot.command()
async def generate_video(ctx, *, prompt: str):
    await ctx.send(f"Generating video for: `{prompt}`... This may take a while.")

    try:
        result = await fal_client.run(
            "fal-ai/ltx-2.3/text-to-video/fast",
            arguments={"prompt": prompt},
        )
        video = result.get("video", {})
        video_url = video.get("url", "")
        if video_url:
            embed = discord.Embed(title="Generated Video", description=prompt)
            embed.set_image(url=video_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("No video was generated.")
    except Exception as e:
        await ctx.send(f"Error generating video: {e}")


bot.run(DISCORD_TOKEN)
