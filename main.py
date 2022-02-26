import io

from Art import Art

import discord
from discord.ext import commands


def main():
    art_text_string = "XQAAAQAABAAAAAAAAAAAbh5RhjiWQJWnRyI9rtRTFHEIieb8urxGUYiJiIyU9+KHoIwF9T1Sw5De5ZSC5Q1/8SR303lFL5nIhy6qnWmTZBIHvr2bdE2ud4vxFgA="
    art = Art(art_text_string=art_text_string)
    print(art)
    print(art.generate_art_text_string())

    """a = [0, 8, 2] * 341 + [0]

    print(art.generate_art_text_string(a))
    art.split_chunked_data()"""

    art.make_art_image_32x32(20).save("output/image32x32.png")
    art.make_art_image_60x24(20).save("output/image60x24.png")

    bot.run("OTQ3MTkwNTAwNDYzNjI0MjMy.Yhpp5Q.zsgiMRI5-faQdwJOvrNYe-xXoQU")


prefix = ">"
bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    print("Everything's all ready to go~")


@bot.event
async def on_message(message):
    print("The message's content was", message.content)
    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    """
    This text will be shown in the help command
    """

    # Get the latency of the bot
    latency = bot.latency  # Included in the Discord.py library
    # Send it to the user
    await ctx.send(str(latency * 1000) + "ms")


@bot.command()
async def echo(ctx, *, content: str):
    await ctx.send(content)


@bot.command()
async def art(ctx, *, content: str):
    print("Kktina z bota: " + content)
    art = Art(art_text_string=content)
    art.make_art_image_60x24(20).save("output/test.png")
    await ctx.send(file=discord.File("output/test.png"))


if __name__ == "__main__":
    main()
