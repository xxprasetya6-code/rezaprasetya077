import tkinter as tk

class SidebarView(tk.Frame):
    def __init__(self, master, on_category_switch, **kwargs):
        super().__init__(master, **kwargs)
        self.on_category_switch = on_category_switch
        self.config(width=200)
        self.pack_propagate(False)
        self.setup_ui()

    def setup_ui(self):
        logo_label = tk.Label(self, text="To Do", font=("Arial", 16, "bold"), bg="#eaeaea", fg="#2564cf")
        logo_label.pack(padx=20, pady=20, anchor="w")

        nav_items = ["My Day", "Important", "Planned", "Tasks"]
        for item in nav_items:
            btn = tk.Button(
                self, 
                text=item, 
                font=("Arial", 11), 
                bg="#eaeaea", 
                bd=0, 
                anchor="w", 
                padx=10, 
                pady=5,
                command=lambda name=item: self.on_category_switch(name)
            )
            btn.pack(fill="x", padx=10, pady=2)