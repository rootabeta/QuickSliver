import asyncio
from sliver import SliverClient
import ttkbootstrap as ttk
from async_tkinter_loop import async_handler, async_mainloop

class ClientWindow(ttk.Frame):
    def __init__(self, app, log, config): #, client):
        super().__init__(app)

        self.log = log
        self.teamserver = (config.lhost, config.lport)
        self.operator = config.operator

        asyncio.run(self._connectClient(config))
        log.info("Connected to teamserver")

        self.root = app
        self.root.deiconify()

        self.root.title(f"QuickSliver -> {self.operator}@{self.teamserver[0]}")
        self.root.geometry("1000x700")

        ttk.Button(self.root, text="Do a thing", command=lambda: asyncio.run(self._test())).pack()
        ttk.Button(self.root, text="Exit", command=self._quit).pack()

        log.debug("Window built")

        self.root.mainloop()
        #async_mainloop(self.root)

    async def _connectClient(self, config):
        self.client = SliverClient(config)
        try:
            await self.client.connect()
        except:
            log.critical("Failed to connect to teamserver")
            exit()

    async def _test(self):
        print("Boop!")

    def _quit(self):
        self.destroy()
        exit()

def launchClient(app, log, config):
    log.info(
        f"Establishing connection to {config.lhost}:{config.lport} as {config.operator}"
    )
#    client = SliverClient(config)
#
#    try:
#        await client.connect()
#    except Exception as e:
#        log.critical("Failed to connect to teamserver")
#        exit()
#
#    log.info("Connected to teamserver")
#    beacons = await client.beacons()
#    sessions = await client.sessions()
#    log.debug(
#        "{} beacons and {} sessions connected".format(len(beacons), len(sessions))
#    )
#
    client = ClientWindow(app, log, config, client)
