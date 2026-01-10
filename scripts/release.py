from functools import partial
from marklidenberg_donyfiles import release
import asyncio

if __name__ == "__main__":
    asyncio.run(release(path=__file__))
