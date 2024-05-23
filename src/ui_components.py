import ttkbootstrap as ttk

class Todo(ttk.Toplevel):
    def __init__(self, app):
        self.title("TODO")
        self.resizable(0,0)
        
        ttk.Label(app, "This is a placeholder").pack()
        ttk.Button(app, "Ok", command=self.destroy)
