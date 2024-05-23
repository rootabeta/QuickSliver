import asyncio
from sliver import SliverClient
import threading


# Wrapper to tell the server to do stuff and hang onto results
class ServerSession:
    def __init__(self, config, log):
        self.config = config
        self.log = log
        self.loop = asyncio.new_event_loop()

        self.loopThread = threading.Thread(target=run_loop, args=(self.loop,))
        self.loopThread.start()

        # Initialize connection to teamserver ASAP
        self._runAsync(self._connectClient)

        self.log.info("Connected to teamserver")

        # Reflect server states
        self.beacons = []
        self.sessions = []

        # For sending events back to the GUI - e.g. beacon called home
        self.events = []

        self.operator = self.config.operator
        self.teamserver = self.config.lhost

        # For debugging
        self.testValue = "Hello from the server!"

        # Launch event handler
        asyncio.run_coroutine_threadsafe(self._handleEvents(), self.loop)

    # Quick skeleton test to respond to a click, do something on the server, and feed the response back where the GUI can grab it
    def test_connection(self):
        self.log.debug("Fetching counts from server")
        self._runAsync(self._updateConnections)
        self.log.debug(f"{len(self.beacons) + len(self.sessions)} agents")

    # Quick skeleton test to respond to a click. Simple as it gets.
    def do_thing(self):
        self.log.debug(f"Someone clicked me! I'm telling mom!")
        self.testValue = "Hey, you clicked me >:c"

    # Continually fetch events from the server
    async def _handleEvents(self):
        self.log.debug("Handling events")
        async for event in self.client.events():
            self.events.append(event)
            match event.EventType:
                case "job-started":
                    self.log.debug("Job started")
                case "job-stopped":
                    self.log.debug("Job stopped")
                case _:
                    self.log.warn(f"Unrecognized event: {event.EventType}")

    # Easy wrapper to run arbitrary functions from sync runtime
    # Results can be ignored or fetched by invoking .fetch() on the returned object
    # Example usage, self._runAsync(self._doStuff, stuffParams)
    def _runAsync(self, function, *args, **kwargs):
        return asyncio.run_coroutine_threadsafe(
            function(*args, **kwargs), self.loop
        ).result()

    # Refresh implant list
    async def _updateConnections(self):
        async with asyncio.TaskGroup() as tg:
            beaconsTask = tg.create_task(self.client.beacons())
            sessionsTask = tg.create_task(self.client.sessions())

        self.beacons = beaconsTask.result()
        self.sessions = sessionsTask.result()

    # Connect to the teamserver and propogate values to window
    async def _connectClient(self):
        # Parse config file and connect to teamserver
        self.client = SliverClient(self.config)
        try:
            await self.client.connect()
            return self.client
        except Exception as e:
            self.client = None
            return None

    def shutdown(self):
        self.log.info("Closing teamserver connection")
        self.loop.call_soon_threadsafe(self.loop.stop)

        # Shut down threads that handle the loop for server comms
        self.loopThread.join()


def run_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
