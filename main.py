import io

from Art import Art

import discord
from discord.ext import commands
from PIL import Image


def main():
    # art_text_string = "XQAAAQAABAAAAAAAAAAAbh5RhjiWQJWnRyI9rtRTFHEIieb8urxGUYiJiIyU9+KHoIwF9T1Sw5De5ZSC5Q1/8SR303lFL5nIhy6qnWmTZBIHvr2bdE2ud4vxFgA="
    # art_text_string = "XQAAAQAABAAAAAAAAAAAagCPB9wf3D0hwPHOSRp24fYRUj2Yyc4qWZjUPZ3Y1KFcqByiF13P4kVX2KIHuKl8SObmDnDfgV+TyV3hmizrUeCdmcHn6yRb469DkPmBai57vCmvmUWgTThPSxj4qM4w60756DP1Ep0l+RjImt/DBeX8FXdw05fgsQCXZyI9LpciC+jlEOTDlwnswTLvXUUV97iuoda2sTqoMedEg50Zm8uZISf0YMlS/ifL2aOohLzw8fLK/y2/67dWp0476ooxGIIEqn3wiI7uMbjmxokcafcUaFgRSVvOmt1nJZoNdUq5/PQ="
    # art = Art(art_text_string=art_text_string)

    # print(art.stringify())
    # print(art)

    # a = [0, 8, 2] * 341 + [0]
    # art = Art(raw_art_data=a)
    # print(art.stringify())
    # print(art)

    # art.make_art_image_32x32(20).save("output/image32x32.png")
    # art.make_art_image_60x24(13).save("output/image60x24.png")

    # artt = art.make_art_image_60x24(13)

    # image = Image.new("RGBA", (984, 837))
    # spaceship = Image.open("./spaceship.png")
    # image.paste(artt, (130, 205), artt)
    # image.save("./result.png")

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
    print("LOG | art to convert: " + content)

    art = Art(art_text_string=content)

    with io.BytesIO() as image_data:
        art.make_art_with_overlay().save(image_data, format="PNG")
        image_data.seek(0)
        file = discord.File(image_data, filename="art.png")

    await ctx.send(file=file)
    file.close()


if __name__ == "__main__":
    main()
