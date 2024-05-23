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

    def refresh(self):
        pass

class Tab(ttk.Frame):
    def __init__(self, parent, text):
        super().__init__(parent)

class TabPanel(ttk.Frame):
    def __init__(self, parent, server):
        super().__init__(parent)


    def addTab(self, tab, title):
        pass

    def removeTab(self, tab):
        pass

    def refresh(self):
        pass
