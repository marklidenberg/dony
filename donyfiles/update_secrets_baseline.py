from marklidenberg_donyfiles import update_secrets_baseline
import asyncio

if __name__ == "__main__":
    asyncio.run(update_secrets_baseline(path=__file__))
