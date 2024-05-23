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

    # Create a TODO popup
    def _TODO(self):
        Todo(self.root)

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
        armoryOptions.add_command(label="Refresh", command=self._TODO)
        armoryOptions.add_command(label="Search", command=self._TODO)

        # Options for the client only
        clientOptions.add_cascade(label="Armory", menu=armoryOptions)
        clientOptions.add_command(label="Exit", command=self._quit)

        # Create a new profile, etc.
        newMenu.add_command(label="Listener")
        newMenu.add_command(label="Profile")
        newMenu.add_command(label="Implant")
        newMenu.add_command(label="Website")

        # View listeners, profiles, etc.
        viewMenu.add_command(label="Jobs")
        viewMenu.add_command(label="Listeners", command=self._addTab)
        viewMenu.add_command(label="Websites")
        viewMenu.add_command(label="Profiles")
        viewMenu.add_command(label="Implants")
        viewMenu.add_command(label="Connections", command=self.server.test_connection)
        viewMenu.add_command(label="Loot")

        # Add top-level menus
        menuBar.add_cascade(label="Client", menu=clientOptions)
        menuBar.add_cascade(label="New", menu=newMenu)
        menuBar.add_cascade(label="View", menu=viewMenu)

        self.root.config(menu=menuBar)

    def _addTab(self, body="Custom tab! Woo!", title="Tab added at runtime!"):
        tab = Tab(self.tabPanel.notebook, body)
        self.tabPanel.addTab(tab, title)

    # Skeleton of the UI - packed into its own function for convenience
    def _buildUI(self):
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.networkGraph = NetworkGraph(self.root, self.server)
        self.networkGraph.grid()

        self.tabPanel = TabPanel(self.root, self.server)
        self.tabPanel.grid()

        # Attach menubar to frame
        self._buildMenuBar()

    # Update the window with fresh data from self.server
    # Only responsible for calling the redraw() methods of its direct descendants
    # Those will, in turn, call their descendants recursively
    # This means invoking this one top-level function will update the entire GUI at once
    # This is done at the configured frame rate (30fps at time of writing) to redraw
    # the entire GUI in "real time" using information from the serversession as-needed
    def redraw(self):
        self.server_events += self.server.events
        self.server.events = []  # Clear out event queue after fetching

        # TODO - We don't want to add new tabs for EVERYTHING
        # But it's a nice PoC
        for event in self.server_events:
            self._addTab(str(event), event.EventType)

        # Your UI redrawing code goes here
        self.networkGraph.refresh()
        self.tabPanel.refresh()

        # Cleanup
        self.server_events = []
        self.root.after(REFRESH_RATE, self.redraw)

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
