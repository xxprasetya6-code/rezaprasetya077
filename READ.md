Dokumentasi Pengujian (Testing Documentation)
Project: Microsoft To Do Clone  
Component: `database.py`, `app.py`, `main_content.py`, `sidebar.py`

1. Proses Pengujian

Ekosistem: Python 3.14 (Menggunakan framework bawaan `unittest`).

Database Pengujian: Pengujian database menggunakan berkas sementara (`test_todo.db`) yang otomatis dibersihkan setiap kali pengujian selesai    (`setUp` & `tearDown`), menjaga database utama (`todo.db`) tetap aman.

(???)Penanganan File OS (Windows): Dilengkapi sistem *delay* (`time.sleep`) dan penangkap pengecualian (`try-except PermissionError`) untuk menghindari kendala penguncian berkas (*file locking*) pada sistem Windows.

2. Struktur Uji (Test Directory)
Seluruh berkas pengujian wajib menggunakan prefiks nama `test_` agar dapat dideteksi secara otomatis oleh test runner.

test_database.py   : Menguji skenario Query & Skema SQLite
test_app.py        : Menguji Logika Controller (Tanpa Render UI)

python app.py 
python -m coverage run -m unittest discover -s tests
python -m coverage report
python -m unittest discover -s tests
