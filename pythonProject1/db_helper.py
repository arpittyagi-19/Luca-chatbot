# db_helper.py
import mysql.connector

cnx = mysql.connector.connect(
    host='127.0.0.1',  # Use 127.0.0.1 instead of localhost
    port=3306,
    user='root',
    password='Tyagi@123456',
    database='pandeyji_eatery'
)


def get_order_status(order_id):
    cursor = cnx.cursor()
    query = "SELECT status FROM order_tracking WHERE order_id = %s"
    cursor.execute(query, (order_id,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None
