from database import get_connection

def add_customer(customer_id, name, email, phone):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO customer (customer_id, name, email, phone) VALUES (%s, %s, %s, %s)",
        (customer_id, name, email, phone)
    )

    conn.commit()
    cur.close()
    conn.close()

    return "Customer added successfully"


def get_customers():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM customer")
    customers = cur.fetchall()

    cur.close()
    conn.close()

    return customers