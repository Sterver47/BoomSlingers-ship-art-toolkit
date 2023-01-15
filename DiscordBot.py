import io
import logging
import random
import time

import discord
from Art import Art, image_to_art

logger = logging.getLogger(__name__)

image_to_art_allowed_channels = ["private-devel"]
image_to_art_allowed_guilds = ["S."]


class Bot(discord.Client):
    __image_to_art_queue: int = 0
    __user_queue: dict[str, list[time.time]] = {}

    @staticmethod
    async def on_ready() -> None:
        logger.info("Discord Bot is ready...")

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
            return  # doesn't respond to itself

        chan_name = str(message.channel)
        guild_name = str(message.guild)
        author_name = str(message.author)

        content_string = str(message.content)

        message_contains_art_string = "XQAAAQAAB" in content_string or "XQAAgAA" in content_string

        if message.attachments or message_contains_art_string:
            await self.change_presence(activity=discord.Game(name="with some art"))

        if message.attachments and (
                chan_name in image_to_art_allowed_channels
                or guild_name in image_to_art_allowed_guilds
                or "Direct Message" in chan_name
        ):
            attachment = message.attachments[0]
            if attachment.filename.lower().endswith((".jpg", ".jpeg", ".png")):
                logger.info(f"Image attachment found in message by {author_name} in #{chan_name}@{guild_name}: {attachment}")
                async with message.channel.typing():
                    await self.make_art_from_image(message)

        elif message_contains_art_string:
            logger.info(f"XQAAAQAAB found in message by {author_name} in #{chan_name}@{guild_name}: {content_string}")
            async with message.channel.typing():
                await make_image_from_artcode(message)

        await self.change_presence(activity=None)

    async def make_art_from_image(self, message: discord.Message) -> None:
        author_name = str(message.author)

        if author_name in self.__user_queue:
            if time.time() - self.__user_queue[author_name][-1] < 30:
                await message.channel.send(
                    "Hmm, I'm sorry. I can't process this image for you now. My Creator didn't want to spend more money on a more powerful server, so he limited me to doing only **1 image per 30 seconds** for you. :smirk: You can ask him how to donate money to improve my servers. However, I think he will only buy more beer with the money you donate. So, Cheers! :beers:")
                return
            self.__user_queue[author_name].append(time.time())
        else:
            self.__user_queue[author_name] = [time.time()]

        self.__image_to_art_queue += 1
        try:
            if self.__image_to_art_queue > 1:
                await message.channel.send(
                    f"Please wait... :timer: I'm currently busy processing {'' if self.__image_to_art_queue > 2 else 'an'}other image{'s' if self.__image_to_art_queue > 2 else ''}. Your image was added to the queue, and I'll process it ASAP. :wink: **Your current position is {self.__image_to_art_queue}.**")
            attachment = message.attachments[0]
            with io.BytesIO() as attachment_data:
                msg = await message.channel.send(f"I'm processing the image you've sent. It may take a while, so please, wait patiently. :slight_smile:")
                await attachment.save(attachment_data)
                art = image_to_art(attachment_data)
                image = art.make_art_with_overlay()
                with io.BytesIO() as image_data:
                    image.save(image_data, format="PNG")
                    image_data.seek(0)
                    file = discord.File(image_data, filename="art.png")
                await message.channel.send(f"Okay, this is all I could do. It's not easy to use only 16 specific colours and this small resolution to achieve perfect results. :sweat_smile: I hope it's not that bad. Actually, if the art looks good, don't forget to share it on the official **Boom Slingers** Discord server *(<#911700820016373791>)*! :v: I'm sending the copyable art code below the image.", file=file)
                file.close()
                await msg.delete()
                await message.channel.send(f"{art.get_art_text_string()}")
        except Exception as e:
            logger.exception(e)
            await message.channel.send("Oh no. Something horrible happened, and I couldn't process the image you've sent. :sob: You can try to contact my Creator Sterver#0769 and tell him about this.")
        self.__image_to_art_queue -= 1


async def make_image_from_artcode(message: discord.Message) -> None:
    words = str(message.content).split()
    art_strings = []
    lowercase_words = []
    for word in words:
        lowercase_words.append(word.lower())
    mirror = True if "mirror" in lowercase_words else False
    for word in words:
        if word.startswith(("XQAAAQAAB", "XQAAgAA")):
            art_strings.append(word)

    if len(art_strings) > 2:
        logger.info(f"{message.author} sent too many art codes in the message: {len(art_strings)}")
        await message.channel.send(
            "Hey! You've sent too many art codes in one message. :face_with_monocle: My Creator decided that I can't convert that many art codes at once, so I will convert only the first two of them. I'm sincerely sorry for his bad decision. :pensive:")
        art_strings = art_strings[:2]

    for art_string in art_strings:
        logger.info(f"Trying to convert '{art_string}' from {message.author}...")
        try:
            art = Art(art_text_string=art_string)
            image = art.make_art_with_overlay(mirror=mirror)
            with io.BytesIO() as image_data:
                image.save(image_data, format="PNG")
                image_data.seek(0)
                file = discord.File(image_data, filename="art.png")
            await message.channel.send(
                f"{str(message.author.mention)} sent this {random.choice(['great', 'fabulous', 'nice', 'marvelous', 'amazing', 'awesome'])} art:\n{' :peace:' if art.seen else ''}",
                file=file)
            file.close()
            if art.smoothing:
                await message.channel.send("Oh, yes, I see the spaceship art is not quite right. It should be smooth. :cow: However, my Creator hasn't implemented a smoothing algorithm in my code. He said it's tough, but I think he's just lazy. Hopefully, he will implement it in the future. Sorry for now. :confused:")
            # await message.channel.send(f"```{art.get_art_text_string()}```")
        except Exception as e:
            await message.channel.send(
                f"Unfortunately, I've struggled with converting the art code you shared into an image. :confused: Please, try to paste it into the in-game paint shop and if it works there, report it to my Creator: Sterver#0769. He probably messed something up in my code... :man_facepalming: The art code I failed to convert was:")
            await message.channel.send(f"```{art_string}```")
            logging.exception(e)
