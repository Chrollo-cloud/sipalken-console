from auth import login_warga, login_petugas
from warga_menu import menu_warga
from admin_menu import menu_admin
from petugas_menu import menu_petugas

while True:
    print("\nSIPALKEN DESA (CONSOLE)")
    print("1. Login Warga")
    print("2. Login Petugas")
    print("0. Keluar")

    pilih = input("Pilih: ")

    if pilih == "1":
        user = login_warga()
        if user:
            menu_warga(user)
        else:
            print("Login gagal")

    elif pilih == "2":
        user = login_petugas()
        if user:
            if user["role"] == "Admin Utama":
                menu_admin()
            else:
                menu_petugas(user)
        else:
            print("Login gagal")

    elif pilih == "0":
        break
