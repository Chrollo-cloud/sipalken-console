from db import get_connection

def menu_petugas(user):
    while True:
        print("\nPETUGAS")
        print("1. Lihat Tugas")
        print("2. Selesaikan Tugas")
        print("0. Logout")

        pilih = input("Pilih: ")

        if pilih == "1":
            lihat_tugas(user["id_petugas"])
        elif pilih == "2":
            selesaikan()
        elif pilih == "0":
            break


def lihat_tugas(id_petugas):
    db = get_connection()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT l.id_laporan, l.deskripsi, l.status
        FROM penugasan p
        JOIN laporan_kerusakan l ON p.id_laporan=l.id_laporan
        WHERE p.id_petugas=%s
    """, (id_petugas,))

    for row in cur.fetchall():
        print(row)

    db.close()


def selesaikan():
    id_laporan = input("ID Laporan: ")
    catatan = input("Catatan selesai: ")

    db = get_connection()
    cur = db.cursor()

    cur.execute("""
        UPDATE laporan_kerusakan
        SET status='Selesai'
        WHERE id_laporan=%s
    """, (id_laporan,))

    cur.execute("""
        INSERT INTO dokumentasi_perbaikan
        (id_laporan, tanggal_selesai, catatan_selesai)
        VALUES (%s, NOW(), %s)
    """, (id_laporan, catatan))

    db.commit()
    db.close()

    print("Laporan selesai")
