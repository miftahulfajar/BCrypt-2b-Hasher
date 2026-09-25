BCrypt 2b Hasher
================

Aplikasi GUI Python sederhana untuk generate dan verify hash password
menggunakan BCrypt 2b.

Fitur:
- Generate hash BCrypt 2b
- Verifikasi password
- Generator password acak 16 karakter
- Copy hash ke clipboard
- Dark/Light mode
- Indikator kekuatan password
- Pilihan cost factor: 8, 10, 12, 14

Kebutuhan:
- Python 3.6+
- Library: bcrypt, pyperclip

  pip install bcrypt pyperclip

Menjalankan:
  python bcrypt_hasher.py

Cara Pakai:
1. Masukkan password.
2. Pilih cost factor.
3. Klik GENERATE HASH.
4. Gunakan COPY atau VERIFY.
5. Klik RANDOM untuk password acak.

Cost Factor:
  8   ~0.01s   Testing
  10  ~0.05s   Cepat
  12  ~0.15s   Default
  14  ~0.6s    Aman

Lisensi:
Bebas digunakan untuk pribadi dan pendidikan.