from __future__ import annotations

import logging

import arrow
import disnake
from disnake.ext import commands

from bot.bot import Bot
from bot.utils.views import DeleteView


logger = logging.getLogger(__name__)


class GatewayLogger(commands.Cog):
    """This is a GatewayLogger."""

    def __init__(self, bot: Bot):
        """Create a GatewayLogger."""
        self.bot = bot

    @commands.Cog.listener()
    async def on_socket_event_type(self, event_type: str) -> None:
        """Log the event."""
        logger.debug(f"Received event {event_type} from the gateway.")
        self.bot.socket_events[event_type] += 1

    async def gateway_events(self, ctx: commands.Context, embed: disnake.Embed, *events: str) -> None:
        """Sends a list of how many times the selected events were received."""
        if len(events) > 25:
            raise commands.CommandError("events must be 25 or less in length.")
        events_and_count = {}
        longest_length = 0
        for event in events:
            event = event.upper()
            longest_length = max(longest_length, len(event))
            count = self.bot.socket_events.get(event.upper(), 0)
            events_and_count[event] = count

        events_and_count = {k: v for k, v in sorted(events_and_count.items(), key=lambda x: x[1], reverse=True)}
        embed.description += "\n"
        for event, count in events_and_count.items():
            embed.description += f"`{event:<{longest_length+1}}`: `{count:>4,}`\n"

        view = DeleteView(ctx.author, allow_manage_messages=False)
        await ctx.send(embed=embed, view=view)

    @commands.command(aliases=("gw",))
    async def gateway(self, ctx: commands.Context, *events: str) -> None:
        """Sends current stats from the gateway."""
        embed = disnake.Embed(title="Gateway Events")

        total_events = sum(self.bot.socket_events.values())
        events_per_second = total_events / (arrow.utcnow() - self.bot.start_time).total_seconds()

        embed.description = f"Start time: {disnake.utils.format_dt(self.bot.start_time.datetime, 'R')}\n"
        embed.description += f"Events per second: `{events_per_second:.2f}`/s\n\u200b"

        if events:
            await self.gateway_events(ctx, embed, *events)
            return

        for event_type, count in self.bot.socket_events.most_common(25):
            embed.add_field(name=event_type, value=f"{count:,}", inline=True)

        view = DeleteView(ctx.author, allow_manage_messages=False)
        await ctx.send(embed=embed, view=view)


def setup(bot: Bot) -> None:
    """Add the gateway logger to the bot."""
    bot.add_cog(GatewayLogger(bot))
