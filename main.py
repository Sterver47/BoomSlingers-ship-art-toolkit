import logging
import sys
from DiscordBot import Bot

file_handler = logging.FileHandler(filename='tmp.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] {%(name)s:%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger(__name__)


def main():
    logger.debug("Creating Bot...")
    bot = Bot()
    logger.info("Starting Bot...")
    bot.run("OTQ3MTkwNTAwNDYzNjI0MjMy.Yhpp5Q.zsgiMRI5-faQdwJOvrNYe-xXoQU")


if __name__ == "__main__":
    main()
