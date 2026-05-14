import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_pharmacast"
    )

def fetch_sales_data(product_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Ambil tanggal dan jumlah penjualan per hari
        query = """
            SELECT sale_date as ds, SUM(quantity) as y 
            FROM sales_items 
            WHERE id_product = %s 
            GROUP BY sale_date 
            ORDER BY sale_date ASC
        """
        cursor.execute(query, (product_id,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except mysql.connector.Error as e:
        raise Exception(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error fetching sales data: {str(e)}")