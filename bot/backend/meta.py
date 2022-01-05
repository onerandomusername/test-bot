import disnake
from disnake.ext import commands

from bot.bot import Bot


class Meta(commands.Cog):
    """Get meta information about the bot."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        """Ping the bot to see its latency and state."""
        embed = disnake.Embed(
            title=":ping_pong: Pong!",
            colour=disnake.Colour.og_blurple(),
            description=f"Gateway Latency: {round(self.bot.latency * 1000)}ms",
        )

        await ctx.send(embed=embed)


def setup(bot: Bot) -> None:
    """Load the Meta cog."""
    bot.add_cog(Meta(bot))
