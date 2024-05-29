import ttkbootstrap as ttk
from tkinter import messagebox

# Dialogue to create new listener on the server
class NewListener(ttk.Toplevel):
    def __init__(self, app, server):
        super().__init__(app)
        self.title("New Listener")

        listenerTypes = [
            "mTLS", # Default has to be listed at [0] - bad design
            "mTLS",
            "HTTP(S)",
            "DNS",
            "WireGuard",
            "Stager"
        ]

        self.lift()
        self.focus_force()
        self.grab_set()

        frame = ttk.Frame(self, width=200, height=600)
        frame.grid(row=0, column=0, padx=10, pady=55)

        selected = ttk.StringVar()
        selected.set(listenerTypes[0])

        self.mTLSFrame = ttk.Frame(frame)
        self.mTLSFrame.grid(row=1, column=0, columnspan=2)

        self.HTTPSFrame = ttk.Frame(frame)
        self.HTTPSFrame.grid(row=1, column=0, columnspan=2)

        self.DNSFrame = ttk.Frame(frame)
        self.DNSFrame.grid(row=1, column=0, columnspan=2)

        self.WGFrame = ttk.Frame(frame)
        self.WGFrame.grid(row=1, column=0, columnspan=2)

        self.StagerFrame = ttk.Frame(frame)
        self.StagerFrame.grid(row=1, column=0, columnspan=2)

        # Populate frames with their options
        ttk.Label(self.mTLSFrame, text="mTLS mode").grid(row=0,column=0)

        ttk.Label(self.HTTPSFrame, text="HTTPS mode").grid(row=0,column=0)
        var = ttk.BooleanVar(value=False)
        ttk.Checkbutton(self.HTTPSFrame, variable=var, text="HTTPS").grid(row=0, column=1)

        ttk.Label(self.DNSFrame, text="DNS mode").grid(row=0,column=0)

        ttk.Label(self.WGFrame, text="WireGuard mode").grid(row=0, column=0)

        ttk.Label(self.StagerFrame, text="Stager mode").grid(row=0, column=0)

        dropDown = ttk.OptionMenu(frame, selected, *listenerTypes, command=self._switchFrame)

        dropDown.grid(
            row=0, column=0, columnspan=2
        )

        cancelButton = ttk.Button(frame, text="Cancel", command=self._cancel).grid(
            row=2, column=0, pady=5, padx=5
        )

        selectbutton = ttk.Button(frame, text="Create", command=self._select).grid(
            row=2, column=1, pady=5, padx=5
        )

        self._switchFrame(listenerTypes[0])
        frame.pack()

    def _switchFrame(self, option):
        print(option)
        match option:
            case "mTLS":
                self.mTLSFrame.grid(row=1, column=0, columnspan=2)

                self.HTTPSFrame.grid_forget()
                self.DNSFrame.grid_forget()
                self.WGFrame.grid_forget()
                self.StagerFrame.grid_forget()
            case "HTTP(S)":
                self.HTTPSFrame.grid(row=1, column=0, columnspan=2)

                self.mTLSFrame.grid_forget()
                self.DNSFrame.grid_forget()
                self.WGFrame.grid_forget()
                self.StagerFrame.grid_forget()
            case "DNS":
                self.DNSFrame.grid(row=1, column=0, columnspan=2)

                self.mTLSFrame.grid_forget()
                self.HTTPSFrame.grid_forget()
                self.WGFrame.grid_forget()
                self.StagerFrame.grid_forget()
            case "WireGuard":
                self.WGFrame.grid(row=1, column=0, columnspan=2)

                self.mTLSFrame.grid_forget()
                self.HTTPSFrame.grid_forget()
                self.DNSFrame.grid_forget()
                self.StagerFrame.grid_forget()
            case "Stager":
                self.StagerFrame.grid(row=1, column=0, columnspan=2)

                self.mTLSFrame.grid_forget()
                self.HTTPSFrame.grid_forget()
                self.DNSFrame.grid_forget()
                self.WGFrame.grid_forget()
            case _:
                messagebox.showwarning(title="Error", message="Invalid listener mode")

    def _select(self):
        # TODO: Send this off to the server
        self.grab_release()
        self.destroy()

    def _cancel(self):
        self.grab_release()
        self.destroy()

