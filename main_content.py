import tkinter as tk

class MainContentView(tk.Frame):
    def __init__(self, master, on_add_task, on_toggle_complete, on_toggle_star, **kwargs):
        super().__init__(master, **kwargs)
        self.on_add_task = on_add_task
        self.on_toggle_complete = on_toggle_complete 
        self.on_toggle_star = on_toggle_star
        self.setup_ui()

    def setup_ui(self):
        self.title_label = tk.Label(self, text="My Day", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.title_label.pack(padx=40, pady=(40, 20), anchor="w")

        self.input_frame = tk.Frame(self, bg="#f3f3f3", height=45)
        self.input_frame.pack(fill="x", padx=40, pady=10)
        self.input_frame.pack_propagate(False)

        plus_label = tk.Label(self.input_frame, text="+", font=("Arial", 16), bg="#f3f3f3", fg="#2564cf")
        plus_label.pack(side="left", padx=10)

        self.entry = tk.Entry(self.input_frame, font=("Arial", 12), bg="#f3f3f3", bd=0, highlightthickness=0)
        self.entry.insert(0, "Add a task")
        self.entry.pack(side="left", fill="both", expand=True, padx=5)
        self.entry.bind("<Button-1>", lambda e: self.entry.delete(0, tk.END) if self.entry.get() == "Add a task" else None)
        self.entry.bind("<Return>", self._handle_submit)

        self.date_entry = tk.Entry(self.input_frame, font=("Arial", 10), bg="#e1e1e1", fg="#555555", bd=0, width=15, justify="center")
        self.date_entry.insert(0, "Add due date")
        self.date_entry.pack(side="right", padx=10, ipady=4)
        self.date_entry.bind("<Button-1>", lambda e: self.date_entry.delete(0, tk.END) if self.date_entry.get() == "Add due date" else None)
        self.date_entry.bind("<Return>", self._handle_submit)

        self.tasks_container = tk.Frame(self, bg="#ffffff")
        self.tasks_container.pack(fill="both", expand=True, padx=40, pady=20)

    def update_header(self, category_name):
        self.title_label.config(text=category_name)

    def clear_task_list(self):
        for widget in self.tasks_container.winfo_children():
            widget.destroy()

    def render_task_row(self, task_id, task_text, is_important, due_date, is_completed):
        task_row = tk.Frame(self.tasks_container, bg="#ffffff", height=45)
        task_row.pack(fill="x", pady=5)
        task_row.pack_propagate(False)

        check_char = "✓" if is_completed else "○"
        text_color = "#a1a1a1" if is_completed else "#333333"
        check_color = "#2564cf" if is_completed else "#797775"

        check_btn = tk.Button(
            task_row, text=check_char, font=("Arial", 12, "bold"), bg="#ffffff", bd=0, fg=check_color, 
            activebackground="#ffffff"
        )
        check_btn.pack(side="left", padx=5)

        text_frame = tk.Frame(task_row, bg="#ffffff")
        text_frame.pack(side="left", fill="both", expand=True, padx=10)

        task_label = tk.Label(text_frame, text=task_text, font=("Arial", 12), bg="#ffffff", fg=text_color)
        task_label.pack(anchor="w", pady=(2, 0))

        check_btn.config(command=lambda: self.on_toggle_complete(task_id, check_btn, task_label))

        if due_date and due_date != "":
            date_color = "#a1a1a1" if is_completed else "#2564cf"
            date_label = tk.Label(text_frame, text=f"📅 {due_date}", font=("Arial", 9), bg="#ffffff", fg=date_color)
            date_label.pack(anchor="w")

        star_char = "★" if is_important else "☆"
        star_color = "#2564cf" if is_important else "#797775"
        
        star_btn = tk.Button(
            task_row, text=star_char, font=("Arial", 14), bg="#ffffff", bd=0, fg=star_color,
            activebackground="#ffffff"
        )
        star_btn.config(command=lambda: self.on_toggle_star(task_id, star_btn))
        star_btn.pack(side="right", padx=10)

    def _handle_submit(self, event):
        task_text = self.entry.get().strip()
        due_text = self.date_entry.get().strip()
        if due_text == "Add due date": due_text = ""

        if task_text and task_text != "Add a task":
            self.on_add_task(task_text, due_text)
            self.entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, "Add due date")