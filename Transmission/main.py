
from transceiver import Transceiver
import asyncio

async def main():
    main_transceiver = Transceiver()
    main_transceiver.transceivers.append(Transceiver())
    main_transceiver.resonation = 200
    await main_transceiver.resonate()

if __name__ == '__main__':
    asyncio.run(main())