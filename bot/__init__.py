import asyncio
import os

from bot import log


try:
    import dotenv
except ModuleNotFoundError:
    raise SystemExit("Could not find python-dotenv. Please install.") from None


if not dotenv.find_dotenv():
    raise SystemExit("No .env file located.")

print("Found .env file, loading environment variables from it.")
dotenv.load_dotenv(override=True)


log.setup()

# Set timestamp of when execution started (approximately)

# On Windows, the selector event loop is required for aiodns.
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
