import asyncio
from sliver import SliverClient
import ttkbootstrap as ttk

class ClientWindow(ttk.Frame):
    def __init__(self, app, log, config, client):
        super().__init__(app)

        self.log = log
        self.teamserver = (config.lhost, config.lport)
        self.operator = config.operator
        self.client = client

        self.root = app
        self.root.deiconify()

        self.root.title(f"QuickSliver -> {self.operator}@{self.teamserver[0]}")
        self.root.geometry("1000x700")

        ttk.Button(self, text="Exit", command=self._quit).pack()

        self.root.mainloop()

    def _quit(self):
        self.destroy()
        exit()

async def launchClient(app, log, config):
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

    client = ClientWindow(app, log, config, client)
