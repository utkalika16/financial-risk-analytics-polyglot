from database import get_connection

def deposit(account_id, amount):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT balance FROM account WHERE account_id = %s",
        (account_id,)
    )

    result = cur.fetchone()

    if result is None:
        cur.close()
        conn.close()
        return "Account not found"

    cur.execute(
        "UPDATE account SET balance = balance + %s WHERE account_id = %s",
        (amount, account_id)
    )

    cur.execute(
        "INSERT INTO transaction (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
        (account_id, "DEPOSIT", amount)
    )

    conn.commit()

    cur.close()
    conn.close()

    return "Deposit successful"


def withdraw(account_id, amount):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT balance FROM account WHERE account_id = %s",
        (account_id,)
    )

    result = cur.fetchone()

    if result is None:
        cur.close()
        conn.close()
        return "Account not found"

    balance = float(result[0])

    if balance < amount:
        cur.close()
        conn.close()
        return "Insufficient balance"

    cur.execute(
        "UPDATE account SET balance = balance - %s WHERE account_id = %s",
        (amount, account_id)
    )

    cur.execute(
        "INSERT INTO transaction (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
        (account_id, "WITHDRAW", amount)
    )

    conn.commit()

    cur.close()
    conn.close()

    return "Withdrawal successful"


def get_transactions():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM transaction")
    transactions = cur.fetchall()

    cur.close()
    conn.close()

    return transactions