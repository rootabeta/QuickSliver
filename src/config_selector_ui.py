import ttkbootstrap as ttk

class ConfigSelector():
    def __init__(self, configs):
        self.selection = None
        self.root = ttk.Window(themename="darkly")

        self.root.title("Select config file")

        options = list(configs.keys())
        options = [options[0]] + options # Set default to first in list
        self.config_name = ttk.StringVar()

        frame = ttk.Frame(self.root, width=200, height=400)
        frame.grid(row=0, column=0, padx=10, pady=55)

        self.dropDown = ttk.OptionMenu(frame, self.config_name, *options).grid(row=0, column=0, columnspan=2, pady=10)
        cancelButton = ttk.Button(frame, text="Cancel", command = self._cancel).grid(row=1, column=0, pady=5)
        selectbutton = ttk.Button(frame, text="Select", command = self._select).grid(row=1, column=1, pady=5)

        frame.pack()
        
        self.root.mainloop()

    def _select(self):
        self.root.destroy()

    def _cancel(self):
        self.root.destroy()
        exit()

def selectConfig(configs):
    config_name = ConfigSelector(configs).config_name.get()

    # Return the item that was selected when the app was closed
    return config_name
