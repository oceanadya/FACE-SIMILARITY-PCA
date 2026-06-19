# === Grafik + Penjelasan (2 Kolom) ===
st.markdown("---")
col_graf, col_exp = st.columns([1, 1])

with col_graf:
    st.subheader("📈 Grafik Akumulasi Informasi")
    explained_variance = np.cumsum(pca.explained_variance_ratio_)
    fig, ax = plt.subplots(figsize=(5, 3.5))  # DIPERKECIL
    ax.plot(range(1, len(explained_variance)+1), explained_variance, 'bo-', linewidth=2, markersize=5)
    ax.axhline(y=0.95, color='red', linestyle='--', linewidth=2, label='95% Varians')
    ax.axhline(y=threshold, color='green', linestyle=':', linewidth=2, label=f'Threshold {threshold:.2f}')
    ax.set_xlabel('Jumlah Komponen PCA (k)', fontsize=10)
    ax.set_ylabel('Akumulasi Informasi', fontsize=10)
    ax.set_title('Kurva Akumulasi Informasi PCA', fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='lower right', fontsize=8)
    ax.set_ylim(0, 1.05)
    st.pyplot(fig)

with col_exp:
    st.subheader("📖 Penjelasan Grafik")
    st.markdown("""
    **Apa itu grafik ini?**
    Grafik ini menunjukkan seberapa banyak **informasi wajah** yang bisa dipertahankan jika kita menggunakan sejumlah komponen PCA (k).

    **Elemen penting:**
    - 🔵 **Garis biru** → kurva akumulasi varians. Semakin tinggi, semakin baik.
    - 🔴 **Garis merah putus-putus** → titik di mana 95% informasi data sudah terwakili. Biasanya kita pilih jumlah komponen di sekitar sini.
    - 🟢 **Garis hijau titik-titik** → **Threshold** (batas kemiripan) yang kamu atur di sidebar. Skor kemiripan ≥ threshold → wajah dianggap **MIRIP**.

    **Cara baca:**
    Misal dengan k = 50, grafik menunjukkan kita sudah mencapai 95% varians. Artinya dari 10.000 pixel, 50 angka sudah cukup mewakili wajah.
    """)
