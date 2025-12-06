# FP_MATDIS_1
Program kalkulator BMR+TDEE dengan streamlit
Kesehatan dan kebugaran tubuh sangat bergantung pada keseimbangan energi, yaitu perbandingan antara kalori yang masuk (makanan) dan kalori yang keluar (aktivitas). Banyak orang kesulitan menentukan porsi makan yang tepat karena tidak mengetahui berapa kebutuhan energi dasar tubuh mereka. Menghitung kebutuhan ini secara manual menggunakan rumus matematika seringkali rentan terhadap kesalahan hitung (human error) dan memakan waktu. Oleh karena itu, diperlukan sebuah program aplikasi sederhana yang dapat menghitung Basal Metabolic Rate (BMR) dan Total Daily Energy Expenditure (TDEE) secara otomatis, akurat, dan cepat.

# Input/Variabel:
  berat (float): Berat badan pengguna dalam satuan Kilogram (kg).
  tinggi (float): Tinggi badan pengguna dalam satuan Centimeter (cm).
  umur (int): Usia pengguna dalam tahun.
  gender (string): Jenis kelamin (Laki-laki/perempuan) yang menentukan konstanta dalam rumus.
  aktivitas (string/int): Pilihan level aktivitas (1-5) yang akan dikonversi menjadi activity multiplier.

# Penjelasan Fungsi:
  hitung_bmr_dan_rumus(berat, tinggi, umur, gender):
    Fungsi ini mengimplementasikan rumus Mifflin-St Jeor. Rumus ini dianggap sebagai salah satu standar paling akurat saat ini untuk menghitung BMR.
    Rumus Dasar: (10 x berat)+(6.25 x tinggi) - (5 x umur) + S
      Di mana S: +5 untuk laki-laki dan -161 untuk perempuan.
    return: hasil BMR, Rumus BMR (untuk kebutuhan visualisasi)
