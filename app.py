# 1. IMPORT MODUL
from flask import Flask, render_template, request, redirect, url_for, abort

# 2. INISIALISASI APLIKASI
app = Flask(__name__)

# 3. PERSIAPAN DATA (Sumber Data Dummy)
# Variabel: TERDAFTAR (Tipe data: List)
TERDAFTAR = ["gara", "indira", "zigma", "arga"]

# Variabel: PROYEK (Tipe data: Dictionary / Kamus)
PROYEK = {
    1: {
        "judul": "Enterprise Network Topology Simulation",
        "kategori": "Network Engineering",
        "status": "Selesai",
        "tahun": 2026
    },
    2: {
        "judul": "Web Vulnerability Lab & PDO Prepared Statements",
        "kategori": "Web Security",
        "status": "Selesai",
        "tahun": 2026
    }
}

# 4. ROUTE STATIS PERTAMA (Halaman Beranda)
@app.route("/")
@app.route("/beranda")
def beranda():
    return render_template("beranda.html", nama="Gara", peran="Network Engineer & IT Support")

@app.route("/proyek")
def daftar_proyek():
    return render_template("proyek.html", data_proyek=PROYEK)

@app.route("/proyek/<int:id>")
def detail_proyek(id):
    # Mengambil data proyek spesifik berdasarkan ID
    item = PROYEK.get(id)
    
    # Validasi: Jika data (ID) tidak ditemukan di dictionary
    if item is None:
        abort(404)  # Memunculkan error 404 Not Found
        
    return render_template("detail_proyek.html", item=item, id=id)

    # ==========================================
# HALAMAN TENTANG & KONTAK
# ==========================================
@app.route("/tentang")
def tentang():
    # Mengirim list keahlian ke HTML
    list_keahlian = ["Network Engineering", "Web Development", "System Troubleshooting"]
    return render_template("tentang.html", keahlian=list_keahlian)

@app.route("/kontak")
def kontak():
    # Mengirim data string email ke HTML
    return render_template("kontak.html", email="gara@sby.centrin.net.id")


# ==========================================
# FITUR CEK USERNAME CLIENT / SYSTEM PROFILE
# ==========================================

# 1. Menangkap data dari form pencarian (Query String)
@app.route("/cek")
def cek_query():
    # Mengambil nilai dari input form yang bernama 'u'
    u = request.args.get("u", "")
    
    # Jika input kosong, kembalikan ke beranda
    if not u:
        return redirect(url_for("beranda"))
        
    # Jika ada isinya, alihkan ke route dinamis di bawah ini
    return redirect(url_for("cek_username", username=u))


# 2. Route Dinamis untuk memproses logika ketersediaan
@app.route("/cek/<username>")
def cek_username(username):
    # Mengubah teks menjadi huruf kecil semua agar seragam
    u = username.lower()
    
    # Logika 1: Username harus minimal 4 karakter (menghasilkan True/False)
    valid = len(u) >= 4
    
    # Logika 2: Cek apakah valid DAN tidak ada di dalam list TERDAFTAR
    tersedia = valid and (u not in TERDAFTAR)
    
    # Melempar 3 variabel ke HTML: username, valid, dan tersedia
    return render_template("cek.html", username=u, valid=valid, tersedia=tersedia)

# ==========================================
# CUSTOM ERROR HANDLER (Pertemuan 9)
# ==========================================
@app.errorhandler(404)
def halaman_tidak_ditemukan(e):
    return render_template("404.html"), 404

# 5. MENJALANKAN SERVER FLASK
if __name__ == "__main__":
    app.run(debug=True)