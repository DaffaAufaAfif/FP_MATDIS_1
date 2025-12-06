import streamlit as st
import pandas as pd
import altair as alt

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Kalkulator BMR & TDEE",
    page_icon="🍎",
    layout="wide"
)

# --- Fungsi Perhitungan & Generator Rumus ---
def hitung_bmr_dan_rumus(berat, tinggi, umur, gender):
    """
    Menghitung BMR sekaligus membuat string LaTeX dinamis
    berdasarkan input user.
    """
    if gender == 'Laki-laki':
        bmr = (10 * berat) + (6.25 * tinggi) - (5 * umur) + 5
        # Rumus Visual Laki-laki
        rumus = r'''
        BMR = (10 \times %s) + (6.25 \times %s) - (5 \times %s) + 5
        ''' % (berat, tinggi, umur)
    else:
        bmr = (10 * berat) + (6.25 * tinggi) - (5 * umur) - 161
        # Rumus Visual Perempuan
        rumus = r'''
        BMR = (10 \times %s) + (6.25 \times %s) - (5 \times %s) - 161
        ''' % (berat, tinggi, umur)
        
    return bmr, rumus

# --- Layout Sidebar (Input) ---
with st.sidebar:
    st.header("📝 Data Diri")
    
    gender = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    berat = st.number_input("Berat Badan (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5)
    tinggi = st.number_input("Tinggi Badan (cm)", min_value=100.0, max_value=250.0, value=170.0, step=1.0)
    umur = st.number_input("Umur (tahun)", min_value=10, max_value=100, value=25, step=1)
    
    st.markdown("---")
    st.header("🏃‍♂️ Tingkat Aktivitas")
    
    # Dictionary Aktivitas
    aktivitas_dict = {
        "Sedentary (Tidak banyak gerak)": 1.2,
        "Lightly Active (1-3 hari/minggu)": 1.375,
        "Moderately Active (3-5 hari/minggu)": 1.55,
        "Very Active (6-7 hari/minggu)": 1.725,
        "Extra Active (Fisik berat/Atlet)": 1.9
    }
    
    pilihan_aktivitas = st.selectbox("Pilih rutinitas Anda saat ini:", list(aktivitas_dict.keys()))
    multiplier_pilihan = aktivitas_dict[pilihan_aktivitas]

# --- Halaman Utama ---
st.title("🍎 Kalkulator Kebutuhan Kalori (TDEE)")
st.markdown("Menghitung **Basal Metabolic Rate (BMR)** dan **Total Daily Energy Expenditure (TDEE)** menggunakan rumus *Mifflin-St Jeor*.")
st.divider()

# 1. Proses Perhitungan
bmr_result, bmr_tex = hitung_bmr_dan_rumus(berat, tinggi, umur, gender)
tdee_result = bmr_result * multiplier_pilihan

# Membuat string LaTeX untuk TDEE secara dinamis
tdee_tex = r'''
TDEE = BMR \times Multiplier \\
TDEE = %.0f \times %.3f
''' % (bmr_result, multiplier_pilihan)

# 2. Tampilkan Hasil Utama (Metrics + Rumus Dinamis)
col1, col2 = st.columns(2)

with col1:
    st.info("### 1. BMR (Basal Metabolic Rate)")
    st.metric(label="Kalori saat istirahat total", value=f"{int(bmr_result):,} kkal")
    
    # --- TAMBAHAN: Rumus Dinamis BMR ---
    st.markdown("**Perhitungan:**")
    st.latex(bmr_tex)
    st.caption("Energi yang dibutuhkan tubuh hanya untuk bernapas dan fungsi organ vital.")

with col2:
    st.success("### 2. TDEE (Kebutuhan Harian)")
    st.metric(label=f"Level: {pilihan_aktivitas.split('(')[0]}", value=f"{int(tdee_result):,} kkal")
    
    # --- TAMBAHAN: Rumus Dinamis TDEE ---
    st.markdown("**Perhitungan:**")
    st.latex(tdee_tex)
    st.caption("Energi total sehari berdasarkan aktivitas fisik yang dipilih.")

st.divider()

# 3. Visualisasi Perbandingan Aktivitas (Chart Altair)
st.subheader("📊 Simulasi Jika Aktivitas Berubah")
st.write("Grafik ini membantu Anda melihat potensi pembakaran kalori jika Anda menambah atau mengurangi aktivitas:")

# Menyiapkan Data untuk Grafik
data_aktivitas = []
for label, mult in aktivitas_dict.items():
    kalori = bmr_result * mult
    # Menandai mana yang dipilih user agar warnanya beda
    status = "Pilihan Anda" if label == pilihan_aktivitas else "Lainnya"
    label_short = label.split(" (")[0] # Mengambil nama depan saja biar grafik rapi
    data_aktivitas.append({
        "Aktivitas": label_short,
        "Kebutuhan Kalori": int(kalori),
        "Status": status
    })

df_chart = pd.DataFrame(data_aktivitas)

# Membuat Chart dengan Altair
chart = alt.Chart(df_chart).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10).encode(
    x=alt.X('Kebutuhan Kalori', title='Kalori (kkal)'),
    y=alt.Y('Aktivitas', sort=list(aktivitas_dict.keys()), title=None),
    color=alt.Color('Status', scale=alt.Scale(domain=['Pilihan Anda', 'Lainnya'], range=['#FF4B4B', '#E0E0E0']), legend=None),
    tooltip=['Aktivitas', 'Kebutuhan Kalori']
).properties(
    height=300
)

# Menampilkan Chart
st.altair_chart(chart, use_container_width=True)

# 4. Rekomendasi Diet
st.divider()
st.subheader("🎯 Target Diet Anda")

col_diet1, col_diet2, col_diet3 = st.columns(3)

with col_diet1:
    st.markdown("#### 🔥 Defisit (Turun Berat)")
    st.write(f"Target: **{int(tdee_result - 500):,} kkal**")
    st.caption("Estimasi turun 0.5kg / minggu")

with col_diet2:
    st.markdown("#### ⚖️ Maintenance (Tetap)")
    st.write(f"Target: **{int(tdee_result):,} kkal**")
    st.caption("Berat badan stabil")

with col_diet3:
    st.markdown("#### 💪 Surplus (Naik Berat)")
    st.write(f"Target: **{int(tdee_result + 500):,} kkal**")
    st.caption("Estimasi naik 0.5kg / minggu")