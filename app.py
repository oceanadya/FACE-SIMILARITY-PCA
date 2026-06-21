import streamlit as st
import halaman.home as home
# import halaman.grayscale as grayscale   # <-- Dinonaktifkan karena kita buat di sini
import halaman.kompresi as kompresi
import halaman.deteksi as deteksi
from PIL import Image, ImageDraw
import io
import base64

st.set_page_config(
    page_title="LANG APP",
    page_icon="🌸",
    layout="wide"
)

# CSS GLOBAL + tambahan untuk profil, card, dll.
st.markdown("""
    <style>
        /* ----- BACKGROUND UTAMA ----- */
        .stApp, .main, .block-container, section.main, div[data-testid="stSidebar"] {
            background-color: #FFF0F5 !important;
            background-image: none !important;
        }
        body, p, div, span, label, h1, h2, h3, h4, h5, h6, .stMarkdown, .stText, .stCaption {
            color: #6A1B4D !important;
        }
        header {
            background: linear-gradient(135deg, #880E4F, #AD1457) !important;
            border-bottom: 2px solid #F8BBD0 !important;
        }
        header * {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }
        .css-1d391kg, .css-12w0qpk, [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FCE4EC, #FFF0F5) !important;
            border-right: 2px solid #F8BBD0 !important;
        }
        .main-title {
            text-align: center !important;
            color: #AD1457 !important;
            font-size: 42px !important;
            font-weight: bold !important;
            text-shadow: 0 2px 15px rgba(173, 20, 87, 0.2) !important;
            display: block !important;
            width: 100% !important;
        }
        .sub-title {
            text-align: center !important;
            color: #D81B60 !important;
            font-size: 18px !important;
            text-shadow: 0 1px 10px rgba(216, 27, 96, 0.15) !important;
            display: block !important;
            width: 100% !important;
        }
        h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
            color: #AD1457 !important;
            font-weight: bold !important;
        }
        .stButton button {
            background: linear-gradient(135deg, #EC407A, #D81B60) !important;
            color: white !important;
            font-size: 18px !important;
            border-radius: 50px !important;
            padding: 10px 30px !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3) !important;
            transition: 0.3s !important;
        }
        .stButton button:hover {
            transform: scale(1.03) translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(233, 30, 99, 0.4) !important;
        }
        div[data-testid="stFileUploader"] {
            background: linear-gradient(135deg, #FCE4EC, #FFF0F5) !important;
            border: 2px dashed #EC407A !important;
            border-radius: 12px !important;
            padding: 10px !important;
        }
        div[data-testid="stFileUploader"] > div {
            background: rgba(255, 255, 255, 0.6) !important;
            border-radius: 8px !important;
            padding: 20px !important;
        }
        div[data-testid="stFileUploader"] * {
            color: #6A1B4D !important;
            background: transparent !important;
        }
        div[data-testid="stFileUploader"] button {
            background: linear-gradient(135deg, #EC407A, #D81B60) !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            padding: 5px 20px !important;
        }
        div[data-testid="stFileUploader"] button:hover {
            transform: scale(1.05) !important;
        }
        div[data-testid="stFileUploader"]:hover {
            border-color: #D81B60 !important;
        }
        .stSlider > div {
            background: rgba(255, 255, 255, 0.4) !important;
            border-radius: 10px !important;
        }
        .pink-badge {
            display: block !important;
            width: 100% !important;
            background: linear-gradient(135deg, #FCE4EC, #F8BBD0) !important;
            color: #AD1457 !important;
            padding: 10px 18px !important;
            border-radius: 12px !important;
            font-weight: bold !important;
            font-size: 16px !important;
            border: 1px solid #EC407A !important;
            box-shadow: 0 2px 10px rgba(233, 30, 99, 0.12) !important;
            text-align: center !important;
            margin-bottom: 12px !important;
        }
        .result-card {
            background: linear-gradient(135deg, #FCE4EC, #FFF0F5) !important;
            padding: 20px !important;
            border-radius: 15px !important;
            text-align: center !important;
            border: 1px solid #F8BBD0 !important;
            box-shadow: 0 4px 15px rgba(233, 30, 99, 0.1) !important;
            height: 100% !important;
        }
        .explanation-box {
            background: rgba(255, 255, 255, 0.5) !important;
            padding: 15px !important;
            border-radius: 12px !important;
            border-left: 4px solid #EC407A !important;
            box-shadow: 0 2px 10px rgba(233, 30, 99, 0.08) !important;
            color: #6A1B4D !important;
        }
        .explanation-box b {
            color: #AD1457 !important;
        }
        .explanation-box ul {
            padding-left: 20px !important;
        }
        .explanation-box li {
            margin-bottom: 6px !important;
        }
        .stSidebar .stButton button {
            width: 48px !important;
            height: 48px !important;
            min-width: 48px !important;
            min-height: 48px !important;
            max-width: 48px !important;
            max-height: 48px !important;
            border-radius: 50% !important;
            border: none !important;
            background: transparent !important;
            font-size: 60px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 !important;
            margin: 0 auto !important;
            box-shadow: none !important;
            transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
            line-height: 1 !important;
        }
        .stSidebar .stButton button:hover {
            transform: scale(1.06) !important;
            background: rgba(236, 64, 122, 0.06) !important;
            box-shadow: 0 0 12px rgba(236, 64, 122, 0.08) !important;
        }
        .sidebar-caption {
            text-align: center;
            color: #AD1457;
            font-weight: bold;
            font-size: 15px;
            padding-top: 5px;
        }

        /* ----- CSS KHUSUS GRAYSCALE ----- */
        .grayscale-header {
            text-align: center;
            padding: 2rem 0 0.5rem 0;
            background: linear-gradient(135deg, #FCE4EC, #FFF0F5);
            border-radius: 20px;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }
        .grayscale-header h1 {
            font-size: 3rem;
            color: #AD1457;
            margin: 0;
            font-weight: 800;
            text-shadow: 2px 2px 10px rgba(173,20,87,0.2);
        }
        .grayscale-header p {
            font-size: 1.2rem;
            color: #6A1B4D;
            margin: 0.5rem 0 1.5rem 0;
        }
        .image-card {
            background: white;
            border-radius: 20px;
            box-shadow: 0 8px 30px rgba(173,20,87,0.12);
            padding: 1.5rem;
            margin: 0.5rem;
            transition: transform 0.3s ease;
            border: 1px solid #F8BBD0;
        }
        .image-card:hover {
            transform: translateY(-5px);
        }
        .image-card h3 {
            color: #AD1457;
            text-align: center;
            margin-bottom: 1rem;
        }
        .image-card img {
            width: 100%;
            border-radius: 12px;
            border: 2px solid #F8BBD0;
        }
        .info-box {
            background: rgba(255,255,255,0.7);
            border-left: 5px solid #EC407A;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin-top: 1.5rem;
            box-shadow: 0 2px 10px rgba(233,30,99,0.08);
        }
        .info-box b {
            color: #AD1457;
        }
        .download-btn {
            background: linear-gradient(135deg, #EC407A, #D81B60);
            color: white;
            border: none;
            border-radius: 50px;
            padding: 0.6rem 2rem;
            font-weight: bold;
            transition: 0.3s;
            box-shadow: 0 4px 15px rgba(233,30,99,0.3);
            cursor: pointer;
        }
        .download-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(233,30,99,0.4);
        }
        .stFileUploader > div {
            background: rgba(255,255,255,0.6) !important;
            border-radius: 12px !important;
            border: 2px dashed #EC407A !important;
        }

        /* Profil tim */
        .profile-card {
            background: white;
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(173,20,87,0.1);
            border: 1px solid #F8BBD0;
        }
        .profile-card h3 {
            color: #AD1457;
            text-align: center;
            margin-bottom: 1rem;
        }
        .profile-item {
            display: flex;
            align-items: center;
            margin-bottom: 0.8rem;
            padding: 0.5rem;
            border-radius: 12px;
            background: #FFF5F8;
        }
        .profile-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, #EC407A, #D81B60);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 20px;
            margin-right: 15px;
            flex-shrink: 0;
        }
        .profile-info {
            flex: 1;
        }
        .profile-info .name {
            font-weight: bold;
            color: #6A1B4D;
        }
        .profile-info .detail {
            font-size: 0.85rem;
            color: #880E4F;
        }

        /* Bunga berjatuhan & efek header */
        .flower-header {
            font-size: 2rem;
            letter-spacing: 8px;
            text-align: center;
            color: #EC407A;
            animation: twinkle 2s infinite alternate;
        }
        @keyframes twinkle {
            0% { opacity: 0.6; transform: scale(1); }
            100% { opacity: 1; transform: scale(1.05); }
        }

        /* Kutipan keren di tengah */
        .quote-box {
            background: linear-gradient(135deg, #FCE4EC, #F8BBD0);
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            margin: 1.5rem 0;
            border-left: 5px solid #EC407A;
            box-shadow: 0 4px 15px rgba(233,30,99,0.1);
        }
        .quote-box p {
            font-size: 1.3rem;
            font-style: italic;
            color: #AD1457;
            margin: 0;
        }
        .quote-box .author {
            font-weight: bold;
            margin-top: 0.5rem;
            font-style: normal;
            color: #880E4F;
        }
    </style>
""", unsafe_allow_html=True)

# Session state
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"
if "show_upload" not in st.session_state:
    st.session_state.show_upload = True
if "grayscale_visited" not in st.session_state:
    st.session_state.grayscale_visited = False

# SIDEBAR NAVIGASI
st.sidebar.markdown("🌸 **Haloo!!**")
menus = [
    ("🏠", "🏠 Home"),
    ("🌫️", "🌫️ Grayscale"),
    ("🗜️", "🗜️ Kompresi"),
    ("🔍", "🔍 Deteksi Kemiripan")
]

cols = st.sidebar.columns(4)
for col, (emoji, page_name) in zip(cols, menus):
    with col:
        is_active = (st.session_state.page == page_name)
        if is_active:
            st.markdown(f"""
                <style>
                    .stSidebar .stButton button[data-testid="baseButton-secondary"]:has(> div:contains("{emoji}")) {{
                        background: #F8BBD0 !important;
                        transform: translateY(2px) scale(1.03) !important;
                        box-shadow: 0 4px 14px rgba(236,64,122,0.25) !important;
                        border: none !important;
                    }}
                </style>
            """, unsafe_allow_html=True)
        if st.button(emoji, key=f"nav_{emoji}", use_container_width=True):
            st.session_state.page = page_name
            if page_name == "🌫️ Grayscale":
                st.session_state.grayscale_visited = False  # reset efek
            st.rerun()

st.sidebar.markdown("---")
if st.session_state.page == "🏠 Home":
    st.sidebar.markdown('<p class="sidebar-caption">📌 Beranda & Profil</p>', unsafe_allow_html=True)
elif st.session_state.page == "🌫️ Grayscale":
    st.sidebar.markdown('<p class="sidebar-caption">🌫️ Ubah ke hitam-putih</p>', unsafe_allow_html=True)
elif st.session_state.page == "🗜️ Kompresi":
    st.sidebar.markdown('<p class="sidebar-caption">🗜️ Kompresi dengan PCA</p>', unsafe_allow_html=True)
elif st.session_state.page == "🔍 Deteksi Kemiripan":
    pass

# ==================== HALAMAN ====================
page = st.session_state.page

if page == "🏠 Home":
    home.tampilkan()

elif page == "🌫️ Grayscale":
    # ---------- HALAMAN GRAYSCALE ----------
    if not st.session_state.grayscale_visited:
        st.balloons()
        st.session_state.grayscale_visited = True

    # Header dengan bunga
    st.markdown("""
    <div class="grayscale-header">
        <div class="flower-header">
            🌸 🌺 🌷 🌹 🌻 🌼 🌸 🌺 🌷 🌹 🌻 🌼
        </div>
        <h1>🌫️ Konversi ke Grayscale</h1>
        <p>Ubah gambar berwarna menjadi hitam-putih dengan mudah.<br> 
        <span style="font-size:0.9rem; color:#880E4F;">✨ Hasil lebih artistik dan fokus pada kontras & tekstur</span></p>
        <div class="flower-header">
            🌸 🌺 🌷 🌹 🌻 🌼 🌸 🌺 🌷 🌹 🌻 🌼
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Layout dua kolom: kiri (utama), kanan (profil + deskripsi fitur + unnes)
    col_left, col_right = st.columns([2, 1], gap="large")

    with col_left:
        # --- Upload ---
        uploaded_file = st.file_uploader(
            "📤 Unggah gambar (JPG, PNG, WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=False
        )

        # --- Kutipan keren di tengah (muncul jika belum upload atau selalu) ---
        st.markdown("""
        <div class="quote-box">
            <p>"Keindahan terletak pada kontras, bukan pada warna."</p>
            <div class="author">— Filosofi Grayscale</div>
            <p style="font-size:1rem; margin-top:0.5rem; color:#6A1B4D;">
                Dengan menghilangkan warna, kita diajak untuk melihat lebih dalam: 
                menangkap tekstur, bentuk, dan emosi murni dari sebuah gambar.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            col1, col2 = st.columns(2, gap="medium")

            with col1:
                st.markdown('<div class="image-card">', unsafe_allow_html=True)
                st.markdown("### 🖼️ Gambar Asli")
                st.image(image, use_container_width=True)
                st.markdown(f"*Ukuran: {image.width} x {image.height} px*")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                if st.button("🔄 Konversi ke Grayscale", use_container_width=True):
                    gray_image = image.convert("L")
                    gray_rgb = gray_image.convert("RGB")

                    st.markdown('<div class="image-card">', unsafe_allow_html=True)
                    st.markdown("### ⚫ Hasil Grayscale")
                    st.image(gray_rgb, use_container_width=True)
                    st.markdown(f"*Ukuran: {gray_rgb.width} x {gray_rgb.height} px*")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Download
                    buf = io.BytesIO()
                    gray_rgb.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    b64 = base64.b64encode(byte_im).decode()
                    href = f'<a href="data:image/png;base64,{b64}" download="grayscale.png" style="text-decoration:none;">'
                    href += '<button class="download-btn">⬇️ Download Hasil</button></a>'
                    st.markdown(href, unsafe_allow_html=True)

                    st.success("🌸 Semoga membantu, terima kasih banyak telah menggunakan jasa layanan kami, salam cinta ❤️")
                    st.balloons()

                    st.markdown("""
                    <div class="info-box">
                        <b>💡 Manfaat Grayscale:</b><br>
                        • Mengurangi kompleksitas warna sehingga fokus pada bentuk dan tekstur.<br>
                        • Menghemat ruang penyimpanan (lebih kecil dari gambar berwarna).<br>
                        • Memberikan nuansa artistik dan klasik pada foto.
                    </div>
                    """, unsafe_allow_html=True)
        else:
            # Placeholder jika belum upload
            st.markdown("""
            <div style="text-align:center; padding:1rem 0;">
                <p style="font-size:1.2rem; color:#6A1B4D;">👆 Unggah gambar untuk mulai mengubahnya menjadi hitam-putih</p>
                <p style="color:#AD1457; opacity:0.7;">Atau gunakan gambar contoh di bawah ini:</p>
            </div>
            """, unsafe_allow_html=True)

            # Contoh gambar
            example_img = Image.new('RGB', (400, 300), color='#FCE4EC')
            draw = ImageDraw.Draw(example_img)
            draw.rectangle([50, 50, 150, 150], fill='#EC407A')
            draw.rectangle([200, 50, 300, 150], fill='#42A5F5')
            draw.rectangle([50, 180, 150, 280], fill='#66BB6A')
            draw.rectangle([200, 180, 300, 280], fill='#FFA726')
            st.image(example_img, caption="Contoh gambar berwarna (unggah gambar Anda sendiri untuk hasil nyata)", use_container_width=True)

    # ---------- KOLOM KANAN ----------
    with col_right:
        # 1. Profil Tim (anggota)
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        st.markdown("### 👥 Tim Pengembang")
        st.markdown("**Teknik Informatika**")

        # Data anggota (ganti dengan data asli)
        anggota = [
            {"nama": "Andi Pratama", "ig": "@andi_p", "telp": "0812-3456-7890"},
            {"nama": "Budi Santoso", "ig": "@budi_s", "telp": "0813-4567-8901"},
            {"nama": "Citra Dewi", "ig": "@citra_d", "telp": "0814-5678-9012"},
            {"nama": "Dian Sastro", "ig": "@dian_s", "telp": "0815-6789-0123"},
        ]

        for idx, member in enumerate(anggota):
            inisial = ''.join([kata[0] for kata in member["nama"].split()])
            st.markdown(f"""
            <div class="profile-item">
                <div class="profile-avatar">{inisial}</div>
                <div class="profile-info">
                    <div class="name">{member['nama']}</div>
                    <div class="detail">📸 {member['ig']}</div>
                    <div class="detail">📞 {member['telp']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # 2. Deskripsi Semua Fitur (Grayscale, PCA, Deteksi) dan Manfaat
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        st.markdown("### 📘 Tentang Aplikasi")
        st.markdown("""
        **Aplikasi LANG** menyediakan tiga fitur utama:
        - **Grayscale** – mengubah gambar berwarna menjadi hitam-putih untuk efek artistik dan mengurangi ukuran file.
        - **Kompresi PCA** – mereduksi dimensi gambar dengan Principal Component Analysis, sehingga ukuran file mengecil tanpa kehilangan banyak informasi.
        - **Deteksi Kemiripan** – membandingkan dua gambar dan menghitung tingkat kemiripannya.
        
        **Manfaat:**
        - Menghemat ruang penyimpanan.
        - Mempermudah analisis visual.
        - Memberikan hasil yang cepat dan akurat.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

        # 3. Universitas
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; color: #AD1457; font-weight: bold; font-size: 1.2rem;">
            🎓 Universitas Negeri Semarang
        </div>
        """, unsafe_allow_html=True)

elif page == "🗜️ Kompresi":
    kompresi.tampilkan()

elif page == "🔍 Deteksi Kemiripan":
    deteksi.tampilkan()
