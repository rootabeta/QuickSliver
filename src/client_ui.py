import asyncio
from sliver import SliverClient
import ttkbootstrap as ttk
import random
import tk_async_execute as tae
import threading

FETCH_RATE = 5 # Fetch fresh data from the server every X seconds to prevent drift
REFRESH_RATE = int(1000 / 30) # Refresh every X ms - should reach frame rate of approx 30fps

class State:
    beacons = 0
    sessions = 0

class ClientWindow(ttk.Frame):
    def __init__(self, app, loop, log, config): #, client):
        super().__init__(app)

        self.variables = {
            "labelValue": "Placeholder"
        }

        # Track variables
        self.loop = loop
        self.log = log
        self.teamserver = (config.lhost, config.lport)
        self.operator = config.operator

        # Initialize window
        self.root = app

        self.label = ttk.Label(text="0")

        # Open teamserver connection
        asyncio.run_coroutine_threadsafe(self._connectClient(config), self.loop)

        ttk.Button(self.root, text="Do a thing", command=self.do_thing).pack()
        ttk.Button(self.root, text="Exit", command=self._quit).pack()

        self.label.pack() # Add label to UI

        self.refresh() # Initialize our local state
        self.redraw() # Prepare to start drawing stuff to screen
        self.log.debug("Client UI window opened")

    async def _do_thing(self):
        beacons = await self.client.beacons()
        print(f"We have {len(beacons)} beacons")
        return len(beacons)

    def do_thing(self):
        asyncio.run_coroutine_threadsafe(self._do_thing(), self.loop)

    async def _asyncCounts(self):
        numBeacons = len(await self.client.beacons())
        numSessions = len(await self.client.sessions())
        string = f"{numBeacons} beacons | {numSessions} sessions"
        self.variables["labelValue"] = string

    def _getCounts(self):
        countFuture = asyncio.run_coroutine_threadsafe(self._asyncCounts(), self.loop)

    def refresh(self):
        self._getCounts()
        self.after(FETCH_RATE * 1000, self.refresh)

    def redraw(self):
        self.label.config(text=self.variables.get("labelValue"))
        self.after(REFRESH_RATE, self.redraw)

    # Connect to the teamserver and propogate values to window
    async def _connectClient(self, config):
        # Parse config file and connect to teamserver
        self.client = SliverClient(config)
        try:
            await self.client.connect()
        except:
            self.log.critical("Failed to connect to teamserver")
            exit()

        # Log success
        self.log.info("Connected to teamserver")

        # Set title
        self.root.title(f"QuickSliver -> {self.operator}@{self.teamserver[0]}")

        # Unhide window after successful connection
        self.root.deiconify()
        # Set window size
        self.root.geometry("1000x700")

    def _quit(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.destroy()
        exit()

def run_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def launchClient(app, log, config):
    log.info(
        f"Establishing connection to {config.lhost}:{config.lport} as {config.operator}"
    )

    # Launch a seperate process to handle asyncio events
    loop = asyncio.new_event_loop()
    loop_thread = threading.Thread(target=run_loop, args=(loop,))
    loop_thread.start()

    client = ClientWindow(app, loop, log, config)
    client.mainloop()

    loop_thread.join()
