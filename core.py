#!/usr/bin/env python3
import asyncio
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NeuraforgeCore:
    async def initialize(self):
        logger.info("🌱 Iniciando NeuraforgeAI Core...")
        # Aquí inicializas tesorería, pagos y bots

    async def run(self):
        while True:
            logger.info("⏳ Ciclo de trabajo...")
            await asyncio.sleep(60)

async def main():
    core = NeuraforgeCore()
    await core.initialize()
    await core.run()

if __name__ == "__main__":
    asyncio.run(main())
