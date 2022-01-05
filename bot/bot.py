import logging
import os

import disnake
from disnake.ext import commands


EXTENSIONS = {}

log = logging.getLogger(__name__)

TEST_GUILDS = os.environ.get("TEST_GUILDS")
if TEST_GUILDS:
    TEST_GUILDS = [int(x.strip()) for x in TEST_GUILDS.split(",")]
    log.info("TEST_GUILDS FOUND")


__all__ = ("Bot", "bot")


class Bot(commands.Bot):
    """Base bot instance."""

    def __init__(self, **kwargs):
        if TEST_GUILDS:
            kwargs["test_guilds"] = TEST_GUILDS
            log.info("registering as test_guilds")
        super().__init__(**kwargs)

    def load_backend_extensions(
        self,
    ) -> None:
        """Load all required backend extensions."""
        self.load_all_extensions("backend")

    def load_all_extensions(self, folder: str) -> None:
        """Load all testing extensions."""
        py_path = f"bot.{folder}"
        og_folder = folder
        folder = f"bot/{og_folder}"
        for name in os.listdir(folder):
            if name.endswith(".py") and os.path.isfile(f"{folder}/{name}"):
                self.load_extension(f"{py_path}.{name[:-3]}")

        log.info(f"Completed loading extensions from {folder}.")

    def add_cog(self, cog: commands.Cog) -> None:
        """
        Delegate to super to register `cog`.

        This only serves to make the info log, so that extensions don't have to.
        """
        super().add_cog(cog)
        log.info(f"Cog loaded: {cog.qualified_name}")


bot = Bot(
    command_prefix=os.environ.get("PREFIX", "="),
    activity=disnake.Game(name=f"Testing: {disnake.__version__}"),
    allowed_mentions=disnake.AllowedMentions.all(),
    intents=disnake.Intents.all(),
)
