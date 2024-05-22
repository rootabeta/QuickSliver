import asyncio
from sliver import SliverClient
import ttkbootstrap as ttk
import random
import threading
from server_session import ServerSession

REFRESH_RATE = int(1000 / 30) # Refresh every X ms - should reach frame rate of approx 30fps

class ClientWindow(ttk.Frame):
    def __init__(self, app, loops, log, config): #, client):
        super().__init__(app)

        # Server event processing should happen on its own dedicated asyncloop
        # This prevents server event floods from consuming GUI events and vice-versa
        self.guiLoop, self.serverLoop = loops
        self.log = log

        # Initialize window
        self.root = app
        
        self.server = ServerSession(config, log, self.serverLoop)
        if not self.server.client:
            console.critical("Failed to establish connection to teamserver")
            self._quit()

        # Add UI elements
        self._buildUI()

        # Finalize GUI now that we're ready to show it to the user
        self.root.title(f"QuickSliver -> {self.server.operator}@{self.server.teamserver}")
        self.root.deiconify()
        self.root.geometry("1000x700")

        self.redraw() # Prepare to start drawing stuff to screen
        self.log.debug("Client UI window opened")

    # Skeleton of the UI - packed into its own function for convenience
    def _buildUI(self):
        self.label = ttk.Label(text="0")

        self.connections = ttk.Label(text="")
        self.connections.pack()

        ttk.Button(self.root, text="Don't click me >:(", command=self.server.do_thing).pack()
        ttk.Button(self.root, text="Get connection counts", command=self.server.test_connection).pack()
        ttk.Button(self.root, text="Exit", command=self._quit).pack()
        self.label.pack() # Add label to UI

    # Update the window with fresh data from self.server
    # Only responsible for calling the redraw() methods of its direct descendants
    # Those will, in turn, call their descendants recursively
    # This means invoking this one top-level function will update the entire GUI at once
    # This is done at the configured frame rate (30fps at time of writing) to redraw
    # the entire GUI in "real time" using information from the serversession as-needed
    def redraw(self):
        self.connections.config(text=f"{len(self.server.beacons)} beacons | {len(self.server.sessions)} sessions")
        self.label.config(text=self.server.testValue) # Test for GUI->client->server->client->GUI round-trip
        self.after(REFRESH_RATE, self.redraw) # Redraw window after however many ms we need to maintain the framerate

    # Called whenever we need to bail out of the GUI for any reason
    # It does all our clean shutdown stuff
    def _quit(self):
        # Shut down event processing
        self.guiLoop.call_soon_threadsafe(self.guiLoop.stop)
        self.server.shutdown()

        # Shut down main window
        self.destroy()

        # Shut down program itself
        exit()

# Super simple event loop processor - just run threads for async stuff forever
def run_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def launchClient(app, log, config):
    log.info(
        f"Establishing connection to {config.lhost}:{config.lport} as {config.operator}"
    )

    # Launch a seperate process to handle asyncio events
    GUI_loop = asyncio.new_event_loop()
    Server_loop = asyncio.new_event_loop()

    tGUI_loop = threading.Thread(target=run_loop, args=(GUI_loop,))
    tServer_loop = threading.Thread(target=run_loop, args=(Server_loop,))

    tGUI_loop.start()
    tServer_loop.start()

    client = ClientWindow(app, (GUI_loop, Server_loop), log, config)
    client.mainloop() # Launch client app

    tGUI_loop.join()
    tServer_loop.join()
