import unittest
import sqlite3
import os
import time
from database import DatabaseManager

class TestTodoDatabase(unittest.TestCase):

    def setUp(self):
        """Runs BEFORE every test. Cleans up stale test files safely."""
        self.test_db_name = "test_todo.db"
        self._safe_remove()
        self.db = DatabaseManager(db_name=self.test_db_name)

    def tearDown(self):
        """Runs AFTER every test. Explicitly releases hooks before deleting."""
        # Force delete the manager reference to free file locks
        if hasattr(self, 'db'):
            del self.db
            
        # Give Windows a brief moment to clear filesystem handles
        time.sleep(0.05)
        self._safe_remove()

    def _safe_remove(self):
        """Helper method to remove the test database without throwing PermissionErrors."""
        if os.path.exists(self.test_db_name):
            try:
                os.remove(self.test_db_name)
            except PermissionError:
                # If Windows is still locking it, ignore it; it will get cleared next run
                pass

    def test_database_initialization(self):
        """Test if the tasks table is successfully created on startup."""
        with sqlite3.connect(self.test_db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
            table_exists = cursor.fetchone()
            
        # ASSERT: The table should exist now (Verified outside connection block)
        self.assertIsNotNone(table_exists)

    def test_add_task(self):
        """Test if adding a task successfully writes to the database."""
        inserted_id, is_important, due_date = self.db.add_task("Buy groceries", "My Day", "Tomorrow")
        
        self.assertEqual(inserted_id, 1)
        self.assertEqual(is_important, 0)
        self.assertEqual(due_date, "Tomorrow")

if __name__ == "__main__":
    unittest.main()