from PyQt5.QtWidgets import QMainWindow, QApplication
import asyncio
from sliver import SliverClient


class ClientWindow(QMainWindow):
    def __init__(self, config, client):
        super().__init__()

        self.teamserver = (config.lhost, config.lport)
        self.operator = config.operator

        self.client = client

        self.buildUI()

        # The 100s are magic numbers :P
        self.setGeometry(100, 100, 1000, 700)

        self.show()

    def buildUI(self):
        # Set window title
        self.setWindowTitle(f"QuickSliver -> {self.operator}@{self.teamserver[0]} ")


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

    app = QApplication([])
    window = ClientWindow(config, client)
    app.exec_()
