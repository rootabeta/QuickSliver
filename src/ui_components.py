import ttkbootstrap as ttk


class Todo(ttk.Toplevel):
    def __init__(self, app):
        super().__init__(app)
        self.title("TODO")
        self.resizable(0, 0)

        ttk.Label(
            self,
            text="This is a placeholder for a feature that hasn't been implemented",
        ).grid()


class NetworkGraph(ttk.Frame):
    def __init__(self, parent, server):
        super().__init__(parent)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.label = ttk.Label(self, text="Network graph goes here")
        self.label.grid()

    def refresh(self):
        pass


class Tab(ttk.Frame):
    def __init__(self, parent, text):
        super().__init__(parent)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.label = ttk.Label(self, text=text)
        self.label.grid()


class TabPanel(ttk.Frame):
    def __init__(self, parent, server):
        super().__init__(parent)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(parent)

        self.tab = Tab(self.notebook, "This is a tab")
        self.tab2 = Tab(self.notebook, "This is another tab")
        self.customTabs = []

        self.notebook.add(self.tab, text="Server")
        self.notebook.add(self.tab2, text="Something else")

        self.notebook.grid()

    def addTab(self, tab, title):
        self.notebook.add(tab, text=title)
        self.customTabs.append(tab)

    def removeTab(self, tab):
        tab.destroy()

    def refresh(self):
        pass
