# app.py - VERSI FINAL (SEMUA TEKS WARNA PUTIH/PINK MUDA)
# =====================================================

import streamlit as st
import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import time

# ==========================================
# 1. PENGATURAN HALAMAN
# ==========================================
st.set_page_config(
    page_title="PCA Face Similarity",
    page_icon="🌸",
    layout="wide"
)

# ==========================================
# 2. CSS - SEMUA TEKS WARNA PUTIH / PINK MUDA
# ==========================================
st.markdown("""
    <style>
        /* ===== BACKGROUND UTAMA ===== */
        .stApp, .main, .block-container, section.main, div[data-testid="stSidebar"] {
            background-color: #6A1B4D !important;
            background-image: none !important;
        }
        
        /* ===== SEMUA TEKS JADI PUTIH / PINK MUDA ===== */
        body, p, div, span, label, h1, h2, h3, h4, h5, h6, 
        .stMarkdown, .stText, .stCaption, .stTitle, .stHeader,
        .stSubheader, .stAlert, .stInfo, .stSuccess, .stError, .stWarning {
            color: #FFE4EC !important;
        }
        
        /* ===== HEADER (BAR ATAS) ===== */
        header {
            background: linear-gradient(135deg, #880E4F, #AD1457) !important;
            border-bottom: 2px solid #F8BBD0 !important;
        }
        
        /* ===== SIDEBAR ===== */
        .css-1d391kg, .css-12w0qpk, [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #6A1B4D, #880E4F) !important;
            border-right: 2px solid #F8BBD0 !important;
        }
        
        /* ===== JUDUL ===== */
        .main-title {
            color: #FFFFFF !important;
            font-size: 42px !important;
            font-weight: bold !important;
            text-shadow: 0 2px 15px rgba(0, 0, 0, 0.3) !important;
            text-align: center !important;
        }
        .sub-title {
            color: #FFE4EC !important;
            font-size: 18px !important;
            text-shadow: 0 1px 10px rgba(0, 0, 0, 0.2) !important;
            text-align: center !important;
        }
        
        /* ===== SEMUA HEADING ===== */
        h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
            color: #FFFFFF !important;
            font-weight: bold !important;
        }
        
        /* ===== FILE UPLOADER ===== */
        div[data-testid="stFileUploader"],
        .stFileUploader,
        .st-emotion-cache-1v0mbdj,
        .st-emotion-cache-1r6slb0,
        .st-emotion-cache-1wmy9hl {
            background: linear-gradient(135deg, #6A1B4D, #880E4F) !important;
            border: 2px dashed #F8BBD0 !important;
            border-radius: 12px !important;
            padding: 10px !important;
        }
        div[data-testid="stFileUploader"] > div,
        .stFileUploader > div {
            background: rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            padding: 20px !important;
        }
        div[data-testid="stFileUploader"] *,
        .stFileUploader * {
            color: #FFE4EC !important;
            background: transparent !important;
        }
        div[data-testid="stFileUploader"] button,
        .stFileUploader button {
            background: linear-gradient(135deg, #EC407A, #D81B60) !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            padding: 5px 20px !important;
        }
        div[data-testid="stFileUploader"] button:hover,
        .stFileUploader button:hover {
            transform: scale(1.05) !important;
        }
        div[data-testid="stFileUploader"]:hover,
        .stFileUploader:hover {
            border-color: #FFFFFF !important;
            background: linear-gradient(135deg, #880E4F, #6A1B4D) !important;
        }
        
        /* ===== TOMBOL SAKURA ===== */
        .sakura-btn-container .stButton button {
            background: transparent !important;
            border: 2px solid #F8BBD0 !important;
            border-radius: 50% !important;
            font-size: 32px !important;
            padding: 8px 14px !important;
            color: #F8BBD0 !important;
            width: 55px !important;
            height: 55px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin: 0 auto !important;
        }
        .sakura-btn-container .stButton button:hover {
            transform: scale(1.1) rotate(15deg) !important;
            background: rgba(248, 187, 208, 0.2) !important;
        }
        
        /* ===== TOMBOL PROSES ===== */
        .stButton button {
            background: linear-gradient(135deg, #EC407A, #D81B60) !important;
            color: white !important;
            font-size: 18px !important;
            border-radius: 50px !important;
            padding: 10px 30px !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        }
        .stButton button:hover {
            transform: scale(1.03) translateY(-2px) !important;
        }
        
        /* ===== METRIC ===== */
        .stMetric {
            background: rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            padding: 10px !important;
        }
        .stMetric label, .stMetric div, .stMetric span {
            color: #FFE4EC !important;
        }
        
        /* ===== SLIDER ===== */
        .stSlider > div {
            background: rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
        }
        
        /* ===== ALERT ===== */
        .stAlert p, .stSuccess p, .stError p, .stWarning p {
            color: #FFFFFF !important;
            font-weight: bold !important;
            font-size: 20px !important;
        }
        .stWarning {
            background-color: rgba(255, 193, 7, 0.2) !important;
            border-radius: 12px !important;
            padding: 5px !important;
        }
        .stWarning p {
            color: #FFFFFF !important;
        }
        .stSuccess {
            background-color: rgba(46, 204, 113, 0.2) !important;
        }
        .stSuccess p {
            color: #FFFFFF !important;
        }
        .stError {
            background-color: rgba(231, 76, 60, 0.2) !important;
        }
        .stError p {
            color: #FFFFFF !important;
        }
        
        /* ===== INFO ===== */
        .stInfo {
            background-color: rgba(52, 152, 219, 0.2) !important;
        }
        .stInfo p {
            color: #FFFFFF !important;
        }
        
        /* ===== BADGE PINK FULL WIDTH ===== */
        .pink-badge {
            display: block !important;
            width: 100% !important;
            background: linear-gradient(135deg, #EC407A, #D81B60) !important;
            color: #FFFFFF !important;
            padding: 10px 18px !important;
            border-radius: 12px !important;
            font-weight: bold !important;
            font-size: 16px !important;
            border: 1px solid #F8BBD0 !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2) !important;
            text-align: center !important;
            margin-bottom: 12px !important;
        }
        .result-container {
            text-align: center !important;
        }
        
        /* ===== PENJELASAN GRAFIK ===== */
        .explanation-box {
            background: rgba(255, 255, 255, 0.1) !important;
            padding: 15px !important;
            border-radius: 12px !important;
            border-left: 4px solid #EC407A !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2) !important;
            color: #FFE4EC !important;
        }
        .explanation-box p, .explanation-box li, .explanation-box b {
            color: #FFE4EC !important;
        }
        .explanation-box ul {
            padding-left: 20px !important;
        }
        .explanation-box li {
            margin-bottom: 6px !important;
        }
        
        /* ===== STREAMLIT DEFAULT ELEMEN ===== */
        .st-emotion-cache-1v0mbdj, .st-emotion-cache-1r6slb0 {
            color: #FFE4EC !important;
        }
        
        /* ===== LABEL ===== */
        .stFileUploader label, .stFileUploader div, .stFileUploader span, .stFileUploader p {
            color: #FFE4EC !important;
        }
        
        /* ===== TEXT INPUT ===== */
        .stTextInput label {
            color: #FFE4EC !important;
        }
        
        /* ===== SELECT BOX ===== */
        .stSelectbox label {
            color: #FFE4EC !important;
        }
        
        /* ===== NUMBER INPUT ===== */
        .stNumberInput label {
            color: #FFE4EC !important;
        }
        
        /* ===== CHECKBOX ===== */
        .stCheckbox label {
            color: #FFE4EC !important;
        }
        
        /* ===== RADIO ===== */
        .stRadio label {
            color: #FFE4EC !important;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SESSION STATE
# ==========================================
if "show_upload" not in st.session_state:
    st.session_state.show_upload = True

# ==========================================
# 4. FUNGSI DETEKSI WAJAH
# ==========================================
def detect_and_crop_face(image_bytes):
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    if len(faces) > 0:
        x, y, w, h = max(faces, key=lambda rect: rect[2] * rect[3])
        return gray[y:y+h, x:x+w], True
    return gray, False

def preprocess_with_face_detection(file_bytes, img_size=(100, 100)):
    face_crop, detected = detect_and_crop_face(file_bytes)
    resized = cv2.resize(face_crop, img_size)
    normalized = resized / 255.0
    return normalized.flatten(), resized, detected

def load_color_image(file_bytes, img_size=(100, 100)):
    np_arr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    if len(faces) > 0:
        x, y, w, h = max(faces, key=lambda rect: rect[2] * rect[3])
        face_crop = img[y:y+h, x:x+w]
        resized = cv2.resize(face_crop, img_size)
        return cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    else:
        resized = cv2.resize(img, img_size)
        return cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

# ==========================================
# 5. JUDUL
# ==========================================
st.markdown('<p class="main-title">🌸 Deteksi Kemiripan Wajah</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Menggunakan PCA (Eigenfaces) & Cosine Similarity</p>', unsafe_allow_html=True)

# ==========================================
# 6. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("---")
    st.markdown('<div class="sakura-btn-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌸", key="toggle_sidebar"):
            st.session_state.show_upload = not st.session_state.show_upload
            st.rerun()
        st.caption("Klik Sakura")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    if st.session_state.show_upload:
        st.header("📂 Upload Data Latih")
        st.markdown("Upload **minimal 10 foto** wajah (2 orang, masing-masing 5+ foto)")
        
        uploaded_train_files = st.file_uploader(
            "Pilih Foto",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="train"
        )
        
        if uploaded_train_files:
            st.success(f"✅ {len(uploaded_train_files)} foto terupload!")
        else:
            st.warning("⬆️ Upload foto di sini")
    else:
        st.info("🌸 Upload disembunyikan. Klik sakura di atas.")
    
    st.divider()
    
    threshold = st.slider("🎯 Ambang Batas Kemiripan", 0.0, 1.0, 0.70, 0.05)
    st.caption(f"Threshold: {threshold:.2f}")
    
    st.divider()
    
    st.markdown("""
        <b>🌸 Kelompok 2</b><br>
        1. Gea Destadia Al-Zahra<br>
        2. Luna Amilia<br>
        3. Dalilah Arifah Ariandi DJR<br>
        4. Nadia Azzizah
    """, unsafe_allow_html=True)

# ==========================================
# 7. AREA UTAMA: UPLOAD 2 FOTO UJI
# ==========================================
st.markdown("## 🔍 Upload Dua Wajah untuk Dibandingkan")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📸 Foto Pertama")
    face1_file = st.file_uploader("Upload Foto 1", type=["jpg","jpeg","png"], key="f1", label_visibility="collapsed")

with col2:
    st.markdown("### 📸 Foto Kedua")
    face2_file = st.file_uploader("Upload Foto 2", type=["jpg","jpeg","png"], key="f2", label_visibility="collapsed")

# ==========================================
# 8. TOMBOL PROSES
# ==========================================
if st.button("🚀 Proses Deteksi Sekarang", use_container_width=True):
    if 'uploaded_train_files' not in locals() or not uploaded_train_files or len(uploaded_train_files) < 10:
        st.error("⚠️ **Data Latih Kurang!** Upload minimal 10 foto.")
        st.info("💡 Klik tombol 🌸 di sidebar untuk menampilkan bagian upload.")
    elif not face1_file or not face2_file:
        st.error("⚠️ Upload kedua foto uji!")
    else:
        with st.spinner("Memproses..."):
            time.sleep(0.5)
            
            IMG_SIZE = (100, 100)
            X_train = []
            progress_bar = st.progress(0)
            for i, file in enumerate(uploaded_train_files):
                vector, _, _ = preprocess_with_face_detection(file.getvalue(), IMG_SIZE)
                X_train.append(vector)
                progress_bar.progress((i+1)/len(uploaded_train_files))
            
            X_train = np.array(X_train)
            k = min(50, len(X_train)-1) if len(X_train)>1 else 1
            pca = PCA(n_components=k)
            X_pca = pca.fit_transform(X_train)
            
            vec1, _, _ = preprocess_with_face_detection(face1_file.getvalue(), IMG_SIZE)
            vec2, _, _ = preprocess_with_face_detection(face2_file.getvalue(), IMG_SIZE)
            
            img1_color = load_color_image(face1_file.getvalue(), IMG_SIZE)
            img2_color = load_color_image(face2_file.getvalue(), IMG_SIZE)
            
            proj1 = pca.transform([vec1])
            proj2 = pca.transform([vec2])
            similarity = cosine_similarity(proj1, proj2)[0][0]
            
            progress_bar.empty()
            
            # ==========================================
            # 9. TAMPILKAN HASIL
            # ==========================================
            st.markdown("---")
            st.subheader("📊 Hasil Deteksi")
            
            col_r1, col_r2, col_r3 = st.columns([2, 2, 1.5])
            
            with col_r1:
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.markdown('<div class="pink-badge">📸 Foto Pertama</div>', unsafe_allow_html=True)
                st.image(img1_color, caption=f"Resize {IMG_SIZE[0]}x{IMG_SIZE[1]}", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_r2:
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.markdown('<div class="pink-badge">📸 Foto Kedua</div>', unsafe_allow_html=True)
                st.image(img2_color, caption=f"Resize {IMG_SIZE[0]}x{IMG_SIZE[1]}", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_r3:
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.markdown('<div class="pink-badge">🎯 Skor Kemiripan</div>', unsafe_allow_html=True)
                st.markdown(f"<h1 style='color:#FFFFFF;font-size:42px;'>{similarity:.2%}</h1>", unsafe_allow_html=True)
                
                if similarity >= threshold:
                    st.success("✅ **MIRIP**")
                    st.balloons()
                elif similarity >= 0.50:
                    st.warning("⚠️ **CUKUP MIRIP**")
                else:
                    st.error("❌ **TIDAK MIRIP**")
                
                st.caption(f"Komponen PCA: {k}")
                st.caption(f"Varians: {np.sum(pca.explained_variance_ratio_)*100:.1f}%")
                st.caption(f"Threshold: {threshold:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # ==========================================
            # 10. GRAFIK + PENJELASAN
            # ==========================================
            st.markdown("---")
            col_graf, col_exp = st.columns([1, 1])
            
            with col_graf:
                st.subheader("📈 Grafik Akumulasi Informasi")
                explained_variance = np.cumsum(pca.explained_variance_ratio_)
                fig, ax = plt.subplots(figsize=(5, 3.5))
                fig.patch.set_facecolor('none')
                ax.set_facecolor('none')
                ax.plot(range(1, len(explained_variance)+1), explained_variance, 'bo-', linewidth=2, markersize=5)
                ax.axhline(y=0.95, color='red', linestyle='--', linewidth=2, label='95% Varians')
                ax.axhline(y=threshold, color='green', linestyle=':', linewidth=2, label=f'Threshold {threshold:.2f}')
                ax.set_xlabel('Jumlah Komponen PCA (k)', fontsize=10, color='white')
                ax.set_ylabel('Akumulasi Informasi', fontsize=10, color='white')
                ax.set_title('Kurva Akumulasi Informasi PCA', fontsize=11, color='white')
                ax.grid(True, alpha=0.3)
                ax.legend(loc='lower right', fontsize=8)
                ax.set_ylim(0, 1.05)
                ax.tick_params(colors='white')
                st.pyplot(fig)
            
            with col_exp:
                st.subheader("📖 Penjelasan Grafik")
                st.markdown("""
                <div class="explanation-box">
                Grafik ini menunjukkan seberapa banyak <b>informasi wajah</b> yang bisa dipertahankan jika menggunakan sejumlah komponen PCA (k).
                
                <br><br>
                
                <b>🔵 Garis biru</b> → kurva akumulasi varians. Semakin tinggi, semakin baik.<br>
                <b>🔴 Garis merah putus-putus</b> → titik 95% informasi data sudah terwakili.<br>
                <b>🟢 Garis hijau titik-titik</b> → <b>Threshold</b> (batas kemiripan) yang kamu atur di sidebar.
                
                <br><br>
                
                <b>💡 Cara baca:</b><br>
                Dari 10.000 pixel wajah, PCA bisa meringkas menjadi 50 angka saja tanpa kehilangan banyak informasi. Semakin tinggi garis biru, semakin baik representasi wajahnya.
                </div>
                """, unsafe_allow_html=True)
