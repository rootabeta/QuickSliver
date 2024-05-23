import asyncio
from sliver import SliverClient
import ttkbootstrap as ttk
import random
import threading
from server_session import ServerSession
from ui_components import *

REFRESH_RATE = int(
    1000 / 30
)  # Refresh every X ms - should reach frame rate of approx 30fps

class ClientWindow(ttk.Frame):
    def __init__(self, app, log, config):  # , client):
        super().__init__(app)

        # Server event processing should happen on its own dedicated asyncloop
        # This prevents server event floods from consuming GUI events and vice-versa
        self.log = log

        # Initialize window
        self.root = app

        self.server = ServerSession(config, log)
        if not self.server.client:
            self.log.critical("Failed to establish connection to teamserver")
            self._quit()

        self.root.protocol("WM_DELETE_WINDOW", self._quit)

        self.server_events = []
        # The server_console window is always open for events and such
        # However, we can have other tabs like for each client
        self.optional_windows = [] 

        # Add UI elements
        self._buildUI()

        # Finalize GUI now that we're ready to show it to the user
        self.root.title(
            f"QuickSliver -> {self.server.operator}@{self.server.teamserver}"
        )
        self.root.deiconify()
        self.root.geometry("1000x700")

        self.redraw()  # Prepare to start drawing stuff to screen
        self.log.debug("Client UI window opened")

    # Build the menu at the top of the screen
    def _buildMenuBar(self):
        # Build main menu bar
        menuBar = ttk.Menu(self.root, tearoff=0) 

        # Create sub-menus
        clientOptions = ttk.Menu(menuBar, tearoff=0)
        newMenu = ttk.Menu(menuBar, tearoff=0)
        viewMenu = ttk.Menu(menuBar, tearoff=0)

        # Armory options
        armoryOptions = ttk.Menu(clientOptions, tearoff=0)
        armoryOptions.add_command(label="Refresh")
        armoryOptions.add_command(label="Search")

        # Options for the client only
        clientOptions.add_cascade(label='Armory', menu=armoryOptions)
        clientOptions.add_command(label='Exit', command=self._quit)

        # Create a new profile, etc.
        newMenu.add_command(label="Listener")
        newMenu.add_command(label="Profile")
        newMenu.add_command(label="Implant")
        newMenu.add_command(label="Website")

        # View listeners, profiles, etc.
        viewMenu.add_command(label="Listeners")
        viewMenu.add_command(label="Websites")
        viewMenu.add_command(label="Profiles")
        viewMenu.add_command(label="Implants")
        viewMenu.add_command(label="Connections")
        viewMenu.add_command(label="Loot")

        # Add top-level menus
        menuBar.add_cascade(label="Client", menu=clientOptions)
        menuBar.add_cascade(label="New", menu=newMenu)
        menuBar.add_cascade(label="View", menu=viewMenu)

        self.root.config(menu = menuBar)
    
    # Skeleton of the UI - packed into its own function for convenience
    def _buildUI(self):
        # Attach menubar to frame
        self._buildMenuBar()

        # Placeholder for *real* stuff
        self.connections = ttk.Label(self.root, text="Awaiting initialization")
        self.connections.pack()

    # Update the window with fresh data from self.server
    # Only responsible for calling the redraw() methods of its direct descendants
    # Those will, in turn, call their descendants recursively
    # This means invoking this one top-level function will update the entire GUI at once
    # This is done at the configured frame rate (30fps at time of writing) to redraw
    # the entire GUI in "real time" using information from the serversession as-needed
    def redraw(self):
        self.server_events += self.server.fetchEvents()

        # Placeholder, show me real time events from server
        self.connections.config(
            text=f"{len(self.server.beacons)} beacons | {len(self.server.sessions)} sessions"
        )

        self.server_events = []

    # Called whenever we need to bail out of the GUI for any reason
    # It does all our clean shutdown stuff
    def _quit(self):
        # Shut down event processing
        self.server.shutdown()

        # Shut down main window
        self.destroy()

        # Shut down program itself
        exit()

def launchClient(app, log, config):
    log.info(
        f"Establishing connection to {config.lhost}:{config.lport} as {config.operator}"
    )

    client = ClientWindow(app, log, config)
    client.mainloop()  # Launch client app
