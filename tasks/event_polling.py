import asyncio
from loguru import logger



async def poll_for_new_events():
    while True:
        logger.info("Polling for new events...")
        #TODO: add polling logic
        await asyncio.sleep(60)
