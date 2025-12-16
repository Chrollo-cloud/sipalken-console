from db import get_connection

def login_warga():
    nik = input("NIK: ")
    password = input("Password: ")

    db = get_connection()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT * FROM warga
        WHERE nik=%s AND password=%s
    """, (nik, password))

    user = cur.fetchone()
    db.close()
    return user

def login_petugas():
    username = input("Username: ")
    password = input("Password: ")

    db = get_connection()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT * FROM petugas
        WHERE username=%s AND password=%s
    """, (username, password))

    user = cur.fetchone()
    db.close()
    return user