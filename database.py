import sqlite3

class DatabaseManager:
    def __init__(self, db_name="todo.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL DEFAULT 'My Day',
                    is_important INTEGER NOT NULL DEFAULT 0,
                    due_date TEXT,
                    is_completed INTEGER NOT NULL DEFAULT 0
                )
            """)
            conn.commit()

    def get_tasks_by_category(self, category):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            if category == "Important":
                cursor.execute("SELECT id, title, is_important, due_date, is_completed FROM tasks WHERE is_important = 1")
            elif category == "Planned":
                cursor.execute("SELECT id, title, is_important, due_date, is_completed FROM tasks WHERE due_date IS NOT NULL AND due_date != ''")
            elif category == "Tasks":
                cursor.execute("SELECT id, title, is_important, due_date, is_completed FROM tasks")
            else:
                cursor.execute("SELECT id, title, is_important, due_date, is_completed FROM tasks WHERE category = ?", (category,))
            return cursor.fetchall()

    def add_task(self, title, category, due_date=None):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            is_imp = 1 if category == "Important" else 0
            if category == "Planned" and (not due_date):
                due_date = "No Date"
            default_cat = "Tasks" if category in ["Important", "Planned"] else category
            
            cursor.execute("INSERT INTO tasks (title, category, is_important, due_date, is_completed) VALUES (?, ?, ?, ?, 0)", 
                           (title, default_cat, is_imp, due_date))
            conn.commit()
            return cursor.lastrowid, is_imp, due_date

    def toggle_completed(self, task_id):
        """Flips completion status between 0 and 1."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET is_completed = 1 - is_completed WHERE id = ?", (task_id,))
            conn.commit()
            cursor.execute("SELECT is_completed FROM tasks WHERE id = ?", (task_id,))
            return cursor.fetchone()[0]

    def toggle_important(self, task_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET is_important = 1 - is_important WHERE id = ?", (task_id,))
            conn.commit()
            cursor.execute("SELECT is_important FROM tasks WHERE id = ?", (task_id,))
            return cursor.fetchone()[0]
        
        # Task category feature