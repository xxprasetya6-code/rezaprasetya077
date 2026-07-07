import tkinter as tk
from database import DatabaseManager
from sidebar import SidebarView
from main_content import MainContentView

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Microsoft To Do Clone")
        self.root.geometry("900x600")
        
        self.db = DatabaseManager()
        self.current_category = "My Day"

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=4)
        self.root.rowconfigure(0, weight=1)

        self.sidebar = SidebarView(self.root, on_category_switch=self.switch_category, bg="#eaeaea")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.main_content = MainContentView(
            self.root, 
            on_add_task=self.add_task, 
            on_toggle_complete=self.toggle_complete, 
            on_toggle_star=self.toggle_star,
            bg="#ffffff"
        )
        self.main_content.grid(row=0, column=1, sticky="nsew")

        self.load_tasks()

    def switch_category(self, category_name):
        self.current_category = category_name
        self.main_content.update_header(category_name)
        self.main_content.clear_task_list()

        if category_name == "Tasks":
            self.main_content.input_frame.pack_forget() # Hides it completely
        else:
            self.main_content.input_frame.pack(fill="x", padx=40, pady=10, after=self.main_content.title_label)

        self.load_tasks()

    def add_task(self, task_text, due_date):
        inserted_id, is_important, final_date = self.db.add_task(task_text, self.current_category, due_date)
        self.main_content.render_task_row(inserted_id, task_text, is_important, final_date, 0)

    def load_tasks(self):
        tasks = self.db.get_tasks_by_category(self.current_category)
        for task_id, title, is_important, due_date, is_completed in tasks:
            self.main_content.render_task_row(task_id, title, is_important, due_date, is_completed)

    def toggle_complete(self, task_id, button_widget, label_widget):
        """Toggles backend complete state and immediately reflects changes on screen visual elements."""
        new_state = self.db.toggle_completed(task_id)
        
        if new_state == 1:
            button_widget.config(text="✓", fg="#2564cf")
            label_widget.config(fg="#a1a1a1")
        else:
            button_widget.config(text="○", fg="#797775")
            label_widget.config(fg="#333333")

    def toggle_star(self, task_id, star_button_widget):
        new_state = self.db.toggle_important(task_id)
        if new_state == 1:
            star_button_widget.config(text="★", fg="#2564cf")
        else:
            star_button_widget.config(text="☆", fg="#797775")
            if self.current_category == "Important":
                star_button_widget.master.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
    # Task category feature