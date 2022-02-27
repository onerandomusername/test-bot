import logging
import os

from bot.bot import bot


log = logging.getLogger(__name__)


bot.load_backend_extensions()
bot.load_all_extensions("cogs")
bot.run(os.environ.get("BOT_TOKEN"))
