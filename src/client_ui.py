import asyncio
from sliver import SliverClient

class ClientWindow():
    def __init__(self, config, client):
        super().__init__()

        self.teamserver = (config.lhost, config.lport)
        self.operator = config.operator

        self.client = client


async def launchClient(log, config):
    log.info(
        f"Establishing connection to {config.lhost}:{config.lport} as {config.operator}"
    )
    client = SliverClient(config)
    try:
        await client.connect()
    except Exception as e:
        log.critical("Failed to connect to teamserver")
        exit()

    log.info("Connected to teamserver")
    beacons = await client.beacons()
    sessions = await client.sessions()
    log.debug(
        "{} beacons and {} sessions connected".format(len(beacons), len(sessions))
    )
