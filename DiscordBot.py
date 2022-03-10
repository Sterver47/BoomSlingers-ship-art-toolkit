import io
import logging
import random

import discord
from Art import Art

logger = logging.getLogger(__name__)


class Bot(discord.Client):
    async def on_ready(self):
        logger.info("Discord Bot is ready...")

    async def on_message(self, message):
        if message.author == self.user:
            return

        content_string = str(message.content)

        if "XQAAAQAAB" in content_string:
            logger.info(f"XQAAAQAAB found in message by {message.author}: {content_string}")

            words = content_string.split()
            art_strings = []
            for word in words:
                if word.startswith("XQAAAQAAB"):
                    art_strings.append(word)

            if len(art_strings) > 2:
                logger.info(f"{message.author} sent too many art codes in the message: {len(art_strings)}")
                await message.channel.send("Hey! You've sent too many art codes in one message. My Creator decided that I can't convert that many art codes at once, so I will convert only the first two of them. I'm sincerely sorry for his bad decision. :pensive:")
                art_strings = art_strings[:2]

            for art_string in art_strings:
                logger.info(f"Trying to convert '{art_string}' from {message.author}...")
                try:
                    art = Art(art_text_string=art_string)
                    with io.BytesIO() as image_data:
                        art.make_art_with_overlay().save(image_data, format="PNG")
                        image_data.seek(0)
                        file = discord.File(image_data, filename="art.png")
                    await message.channel.send(f"{str(message.author.mention)} sent this {random.choice(['great', 'fabulous', 'nice'])} art:\n(copyable code is below the image)", file=file)
                    await message.channel.send(f"```{art_string}```")
                    file.close()
                except Exception as e:
                    await message.channel.send(f"Unfortunately, I struggled with converting the art code you shared to an image. Please, try to paste it into the in-game paint shop and if it works there, report it to my Creator: Sterver#0769. He probably messed something up in my code... :man_facepalming: The art code I failed to convert was:")
                    await message.channel.send(f"```{art_string}```")
                    logging.exception(e)
