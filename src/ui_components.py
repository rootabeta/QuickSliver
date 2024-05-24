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

        self.label = ttk.Label(self, text="Foo")
        self.label.pack(expand=True, fill='both')

    def refresh(self):
        pass

class Tab(ttk.Frame):
    def __init__(self, parent, body):
        super().__init__(parent)

        self.label = ttk.Label(self, text=body)
        self.label.pack(expand=True, fill='both')

class TabPanel(ttk.Frame):
    def __init__(self, parent, server):
        super().__init__(parent)

        #self.label = ttk.Label(self, text="Bar")
        #self.label.pack(expand=True, fill='both')

        self.notebook = ttk.Notebook(self)

        tab1 = Tab(self.notebook, "First tab")
        tab2 = Tab(self.notebook, "Second tab")
        
        self.notebook.add(tab1, text="One")
        self.notebook.add(tab2, text="Two")

        self.notebook.pack(expand=True, fill='both')

    def addTab(self, tab, title):
        self.notebook.add(tab, text=title)
        self.notebook.select(tab) # Focus on new tab

    def removeTab(self, tab):
        pass

    def refresh(self):
        pass
