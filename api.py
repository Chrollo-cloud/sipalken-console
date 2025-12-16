from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_connection

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "API SIPALKEN RUNNING"


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    role = data["role"]
    username = data["username"]
    password = data["password"]

    db = get_connection()
    cur = db.cursor(dictionary=True)

    user = None

    if role == "warga":
        cur.execute(
            "SELECT id_warga, nama FROM warga WHERE nik=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()

    elif role in ["admin", "petugas"]:
        cur.execute(
            "SELECT id_petugas, nama, nama FROM petugas WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()

    db.close()

    if not user:
        return jsonify({"success": False}), 401

    return jsonify({"success": True, "user": user})



@app.route("/laporan", methods=["GET", "POST"])
def laporan():
    db = get_connection()
    cur = db.cursor(dictionary=True)

    
    if request.method == "GET":
        cur.execute("""
            SELECT l.id_laporan, w.nama AS warga, l.deskripsi, l.status
            FROM laporan_kerusakan l
            JOIN warga w ON l.id_warga = w.id_warga
            ORDER BY l.id_laporan DESC
        """)
        data = cur.fetchall()
        db.close()
        return jsonify(data)

    
    if request.method == "POST":
        data = request.json
        cur.execute("""
            INSERT INTO laporan_kerusakan
            (id_warga, id_kategori, id_lokasi, tanggal_lapor, deskripsi, status)
            VALUES (%s,%s,1,NOW(),%s,'Menunggu Verifikasi')
        """, (
            data["id_warga"],
            data["id_kategori"],
            data["deskripsi"]
        ))
        db.commit()
        db.close()
        return jsonify({"success": True})



@app.route("/laporan/<int:id>/status", methods=["PUT"])
def update_status(id):
    data = request.json
    db = get_connection()
    cur = db.cursor()

    cur.execute(
        "UPDATE laporan_kerusakan SET status=%s WHERE id_laporan=%s",
        (data["status"], id)
    )

    db.commit()
    db.close()
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
