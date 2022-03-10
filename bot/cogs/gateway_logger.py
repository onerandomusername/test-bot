from __future__ import annotations

import logging

from disnake.ext import commands

from bot.bot import Bot


logger = logging.getLogger(__name__)


class GatewayLogger(commands.Cog):
    """This is a GatewayLogger."""

    def __init__(self, bot: Bot):
        """Create a GatewayLogger."""
        self.bot = bot

    @commands.Cog.listener()
    async def on_socket_event_type(self, event: str) -> None:
        """Log the event."""
        logger.debug(f"Received event {event} from the gateway.")


def setup(bot: Bot) -> None:
    """Add the gateway logger to the bot."""
    bot.add_cog(GatewayLogger(bot))
