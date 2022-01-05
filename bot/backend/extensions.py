from disnake import DiscordException
from disnake.ext import commands

from bot.bot import Bot


class ExtensionManager(commands.Cog):
    """Manage extensions."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(aliases=("rl", "r"))
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, ext: str) -> None:
        """Reload the provided extension."""
        # validate ext is in extension
        for e in self.bot.extensions:
            if e.endswith(ext):
                break
        else:
            await ctx.send(f"Sorry, {ext} is not a valid extension.")
            return
        try:
            self.bot.reload_extension(e)
        except DiscordException as err:
            await ctx.send(f"```\n{err}```")
        else:
            await ctx.send(f"Successfully reloaded {e}")


def setup(bot: Bot) -> None:
    """Add the extension manager to the bot."""
    bot.add_cog(ExtensionManager(bot))
