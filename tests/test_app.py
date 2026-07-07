import unittest
import tkinter as tk
import os
from app import TodoApp

class TestTodoApp(unittest.TestCase):
    def setUp(self):
        # Setup a temporary root window and redirect the app to a test database
        self.root = tk.Tk()
        # Withdraw hides the window from physically popping up on your screen during tests!
        self.root.withdraw() 
        
        self.app = TodoApp(self.root)
        # Override database to a safe test file name
        self.app.db.db_name = "test_app_todo.db"
        self.app.db.init_db()

    def tearDown(self):
        self.root.destroy()
        if os.path.exists("test_app_todo.db"):
            try:
                os.remove("test_app_todo.db")
            except PermissionError:
                pass

    def test_switch_category(self):
        """Test if switching categories correctly updates the state."""
        # Act: Switch to Planned category
        self.app.switch_category("Planned")
        
        # Assert: Check if the application state changed properly
        self.assertEqual(self.app.current_category, "Planned")
        self.assertEqual(self.app.main_content.title_label.cget("text"), "Planned")