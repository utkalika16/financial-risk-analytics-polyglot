from database import get_connection

def add_account(account_id, customer_id, account_type, balance):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO account (account_id, customer_id, account_type, balance) VALUES (%s, %s, %s, %s)",
        (account_id, customer_id, account_type, balance)
    )

    conn.commit()
    cur.close()
    conn.close()

    return "Account added successfully"


def get_accounts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM account")
    accounts = cur.fetchall()

    cur.close()
    conn.close()

    return accounts

def delete_account(account_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT account_id FROM account WHERE account_id = %s", (account_id,))
    if cur.fetchone() is None:
        cur.close()
        conn.close()
        return "Account not found"

    cur.execute("DELETE FROM transaction WHERE account_id = %s", (account_id,))
    cur.execute("DELETE FROM account WHERE account_id = %s", (account_id,))

    conn.commit()
    cur.close()
    conn.close()

    return "Account deleted successfully"
