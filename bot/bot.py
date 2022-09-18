import collections
import inspect
import logging
import os

import arrow
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

        # due to disnake#371, pop all kwargs that aren't received by the super
        if kwargs.pop("allow_extraneous_arguments", False) is True:
            all_params = set()
            for cls in self.__class__.__mro__:
                if not hasattr(cls, "__init__"):
                    continue
                sig = inspect.signature(cls.__init__)
                all_params.update(
                    name
                    for name, param in sig.parameters.items()
                    if param.kind in (inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
                )
            kwargs = {k: v for k, v in kwargs.items() if k in all_params}
        super().__init__(**kwargs)

        self.socket_events = collections.Counter()
        self.start_time: arrow.Arrow = arrow.utcnow()

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
                if name.startswith("_"):
                    # ignore all files that start with _
                    continue
                self.load_extension(f"{py_path}.{name[:-3]}")

        log.info(f"Completed loading extensions from {folder}.")

    def add_cog(self, cog: commands.Cog) -> None:
        """
        Delegate to super to register `cog`.

        This only serves to make the info log, so that extensions don't have to.
        """
        super().add_cog(cog)
        log.info(f"Cog loaded: {cog.qualified_name}")

    async def login(self, token: str) -> None:
        """Login to discord and set the intents."""
        await super().login(token)
        info = await self.application_info()
        flags = info.flags
        if flags:
            intents = self._real_intents
            intents.members = flags.gateway_guild_members or flags.gateway_guild_members_limited
            intents.presences = flags.gateway_presence or flags.gateway_presence_limited
            if hasattr(intents, "message_content"):
                intents.message_content = flags.gateway_message_content or flags.gateway_message_content_limited

            self._connection.member_cache_flags = disnake.MemberCacheFlags.from_intents(intents)
            self._connection._chunk_guilds = intents.members

    @property
    def _real_intents(self) -> disnake.Intents:
        return self._connection._intents

    async def on_connect(self) -> None:
        """Print the session start limit on connection."""
        print(self.session_start_limit)


_intents = disnake.Intents.all()
# _intents.message_content = False

kwargs = {}
if hasattr(disnake, "ApplicationCommandSyncFlags"):
    kwargs["command_sync"] = commands.ApplicationCommandSyncFlags.all()
else:
    kwargs["sync_commands_debug"] = True
    kwargs["sync_commands"] = True
kwargs["allow_extraneous_arguments"] = True

if hasattr(disnake, "GatewayParams"):
    kwargs["gateway_params"] = disnake.GatewayParams(zlib=True)

bot = Bot(
    command_prefix=commands.when_mentioned_or(os.environ.get("PREFIX", "=")),
    activity=disnake.Game(name=f"Testing: {disnake.__version__}"),
    allowed_mentions=disnake.AllowedMentions.all(),
    intents=_intents,
    **kwargs,
)
