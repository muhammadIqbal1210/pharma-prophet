import mysql.connector
from datetime import datetime, timedelta
import random

def seed_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="", # Kosongkan jika pakai XAMPP default
        database="db_pharmacast"
    )
    cursor = conn.cursor()

    # Membuat tabel jika belum ada
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            nama_lengkap VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_product INT,
            sale_date DATE,
            quantity INT
        )
    """)

    product_id = 1
    start_date = datetime.now() - timedelta(days=365)
    
    print("Mengisi data simulasi ke MySQL...")
    
    for i in range(365):
        current_date = start_date + timedelta(days=i)
        # Simulasi penjualan harian (10-30 unit)
        quantity = random.randint(10, 30)
        
        cursor.execute(
            "INSERT INTO sales_items (id_product, sale_date, quantity) VALUES (%s, %s, %s)",
            (product_id, current_date.date(), quantity)
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("Selesai! Data simulasi berhasil dimasukkan.")

if __name__ == "__main__":
    seed_data()