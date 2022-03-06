import io
import discord
from Art import Art

class Bot(discord.Client):
    async def on_ready(self):
        print("Everything's all ready to go~")

    async def on_message(self, message):
        if message.author == self.user:
            return

        content = message.content

        print("The message's content was", content)

        if content.startswith("XQAAA"):
            print("LOG | art to convert: " + content)

            art = Art(art_text_string=content)

            with io.BytesIO() as image_data:
                art.make_art_with_overlay().save(image_data, format="PNG")
                image_data.seek(0)
                file = discord.File(image_data, filename="art.png")

            await message.channel.send("This is your art", file=file)
            file.close()
