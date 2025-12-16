from db import get_connection
from datetime import datetime

def menu_warga(user):
    while True:
        print("\nMENU WARGA")
        print("1. Buat Laporan")
        print("2. Lihat Laporan Saya")
        print("0. Logout")

        pilih = input("Pilih: ")

        if pilih == "1":
            buat_laporan(user["id_warga"])
        elif pilih == "2":
            lihat_laporan(user["id_warga"])
        elif pilih == "0":
            break



def buat_laporan(id_warga):
    id_kategori = input("ID Kategori: ")
    id_lokasi = input("ID Lokasi: ")
    deskripsi = input("Deskripsi Kerusakan: ")

    db = get_connection()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO laporan_kerusakan
        (id_warga, id_kategori, id_lokasi, tanggal_lapor, deskripsi)
        VALUES (%s, %s, %s, %s, %s)
    """, (id_warga, id_kategori, id_lokasi, datetime.now(), deskripsi))

    db.commit()
    db.close()
    print("Laporan berhasil dikirim (Menunggu Verifikasi)")


def lihat_laporan(id_warga):
    db = get_connection()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT id_laporan, deskripsi, status
        FROM laporan_kerusakan
        WHERE id_warga=%s
    """, (id_warga,))

    for row in cur.fetchall():
        print(row)
    
    db.close()
    