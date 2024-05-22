import asyncio
from sliver import SliverClient


# Wrapper to tell the server to do stuff and hang onto results
class ServerSession:
    def __init__(self, config, log, loop):
        self.config = config
        self.log = log
        self.loop = loop

        # Initialize connection to teamserver ASAP
        self._runAsync(self._connectClient)

        # Log success
        self.log.info("Connected to teamserver")

        self.operator = self.config.operator
        self.teamserver = self.config.lhost

        # For debugging
        self.testValue = "Hello from the server!"

        # Reflect server states
        self.beacons = []
        self.sessions = []

    async def _updateConnections(self):
        async with asyncio.TaskGroup() as tg:
            beaconsTask = tg.create_task(self.client.beacons())
            sessionsTask = tg.create_task(self.client.sessions())

        self.beacons = beaconsTask.result()
        self.sessions = sessionsTask.result()

    # Quick skeleton test to respond to a click, do something on the server, and feed the response back where the GUI can grab it
    def test_connection(self):
        self.log.debug("Fetching counts from server")
        self._runAsync(self._updateConnections)
        self.testValue = f"{len(self.beacons) + len(self.sessions)} agents"

    def do_thing(self):
        self.log.debug(f"Someone clicked me! I'm telling mom!")
        self.testValue = "Hey, you clicked me >:c"

    # Easy wrapper to run arbitrary functions from sync runtime
    # Results can be ignored or fetched by invoking .fetch() on the returned object
    # Example usage, self._runAsync(self._doStuff, stuffParams)
    def _runAsync(self, function, *args, **kwargs):
        return asyncio.run_coroutine_threadsafe(
            function(*args, **kwargs), self.loop
        ).result()

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
