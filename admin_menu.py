from db import get_connection
from datetime import datetime

def menu_admin():
    while True:
        print("\n ADMIN UTAMA")
        print("1. Lihat Laporan Masuk")
        print("2. Verifikasi Laporan")
        print("3. Buat Penugasan")
        print("0. Logout")

        pilih = input("Pilih: ")
        
        if pilih == "1":
            lihat_laporan()
        elif pilih == "2":
            verifikasi()
        elif pilih == "3":
            buat_penugasan()
        elif pilih == "0":
            break


def lihat_laporan():
    db = get_connection()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT id_laporan, deskripsi, status
        FROM laporan_kerusakan
    """)

    for row in cur.fetchall():
        print(row)

    db.close()

def verifikasi():
    id_laporan = input("ID Laporan: ")
    catatan = input("Catatan Verifikasi: ")

    db = get_connection()
    cur = db.cursor()

    cur.execute("""
        UPDATE laporan_kerusakan
        SET status='Terverifikasi',
            tanggal_verifikasi=%s,
            catatan_verifikasi=%s
        WHERE id_laporan=%s
    """, (datetime.now(), catatan, id_laporan))

    db.commit()
    db.close()
    print("LAPORAN DIVERIFIKASI")

def buat_penugasan():
    id_laporan = input("ID Laporan: ")
    id_petugas = input("ID Petugas: ")

    db = get_connection()
    cur = db.cursor()
    
    cur.execute("""
        INSERT INTO penugasan
        (id_laporan, id_petugas, tanggal_mulai)
        VALUES (%s, %s, NOW())
    """, (id_laporan, id_petugas))

    db.commit()
    db.close()
    print("Penugasan Dibuat (Trigger Aktif)")