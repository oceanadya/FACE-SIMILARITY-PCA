# app.py - VERSI FINAL (File Uploader Pink Total)
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
# 1. PENGATURAN HALAMAN & CSS
# ==========================================
st.set_page_config(
    page_title="PCA Face Similarity",
    page_icon="🌸",
    layout="wide"
)

st.markdown("""
    <style>
        /* ===== BACKGROUND UTAMA ===== */
        .stApp {
            background: linear-gradient(135deg, #FFF0F5, #FFE4E9, #FCE4EC) !important;
        }
        .main > div {
            background: transparent !important;
        }
        
        /* ===== HEADER / TOP BAR (PINK GELAP) ===== */
        header {
            background: linear-gradient(135deg, #880E4F, #AD1457, #880E4F) !important;
            border-bottom: 2px solid #F8BBD0 !important;
            box-shadow: 0 2px 15px rgba(136, 14, 79, 0.3) !important;
        }
        
        /* ===== SIDEBAR (PINK SOFT) ===== */
        .css-1d391kg, .css-12w0qpk, [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FCE4EC 0%, #FFF0F5 100%) !important;
            border-right: 2px solid #F8BBD0 !important;
        }
        
        /* ===== JUDUL UTAMA ===== */
        .main-title {
            text-align: center;
            color: #AD1457 !important;
            font-size: 42px !important;
            font-weight: bold !important;
            text-shadow: 0 2px 15px rgba(173, 20, 87, 0.2) !important;
        }
        .sub-title {
            text-align: center;
            color: #D81B60 !important;
            font-size: 18px !important;
            text-shadow: 0 1px 10px rgba(216, 27, 96, 0.15) !important;
        }
        
        /* ===== TULISAN DI AREA UTAMA ===== */
        h1, h2, h3, h4, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
            color: #AD1457 !important;
        }
        
        /* ===== FILE UPLOADER (KOTAK PUTUS-PUTUS) ===== */
        .stFileUploader > div:first-child {
            background: linear-gradient(135deg, #FFF0F5, #FCE4EC) !important;
            border: 2px dashed #EC407A !important;
            border-radius: 15px !important;
            padding: 20px !important;
            transition: 0.3s !important;
        }
        .stFileUploader > div:first-child:hover {
            background: #FFF5F7 !important;
            border-color: #D81B60 !important;
            box-shadow: 0 0 20px rgba(236, 64, 122, 0.15) !important;
        }
        
        /* ===== TEKS DI DALAM FILE UPLOADER ===== */
        .stFileUploader > div:first-child p {
            color: #AD1457 !important;
            font-weight: 500 !important;
        }
        .stFileUploader > div:first-child small {
            color: #D81B60 !important;
        }
        .stFileUploader > div:first-child button {
            background: linear-gradient(135deg, #EC407A, #D81B60) !important;
            color: white !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 8px 20px !important;
            transition: 0.3s !important;
        }
        .stFileUploader > div:first-child button:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3) !important;
        }
        
        /* ===== DRAG AND DROP TEXT ===== */
        .stFileUploader > div:first-child div:first-child {
            color: #AD1457 !important;
            font-size: 16px !important;
        }
        
        /* ===== BATAS FILE (JPG, PNG) ===== */
        .stFileUploader > div:first-child div:last-child {
            color: #D81B60 !important;
            font-size: 13px !important;
        }
        
        /* ===== CARD HASIL ===== */
        .result-card {
            background: linear-gradient(135deg, #FCE4EC, #FFF0F5);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid #F8BBD0;
            box-shadow: 0 4px 15px rgba(233, 30, 99, 0.1);
        }
        
        /* ===== TOMBOL PROSES ===== */
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
        
        /* ===== SLIDER ===== */
        .stSlider > div {
            background: rgba(255, 255, 255, 0.4) !important;
            border-radius: 10px !important;
        }
        
        /* ===== METRIC ===== */
        .stMetric {
            background: rgba(255, 255, 255, 0.3) !important;
            border-radius: 12px !important;
            padding: 10px !important;
        }
        
        /* ===== TOMBOL SAKURA DI SIDEBAR ===== */
        .stSidebar .stButton button {
            background: transparent !important;
            border: 2px solid #EC407A !important;
            border-radius: 50% !important;
            font-size: 32px !important;
            padding: 8px 14px !important;
            transition: 0.3s !important;
            color: #EC407A !important;
            box-shadow: none !important;
        }
        .stSidebar .stButton button:hover {
            transform: scale(1.1) rotate(15deg) !important;
            background: rgba(236, 64, 122, 0.2) !important;
            box-shadow: 0 0 20px rgba(236, 64, 122, 0.3) !important;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE
# ==========================================
if "show_upload" not in st.session_state:
    st.session_state.show_upload = True

# ==========================================
# 3. FUNGSI DETEKSI WAJAH
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

# ==========================================
# 4. JUDUL
# ==========================================
st.markdown('<p class="main-title">🌸 Deteksi Kemiripan Wajah</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Menggunakan PCA (Eigenfaces) & Cosine Similarity</p>', unsafe_allow_html=True)

# ==========================================
# 5. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌸", key="toggle_sidebar"):
            st.session_state.show_upload = not st.session_state.show_upload
            st.rerun()
        st.caption("Klik Sakura")
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
# 6. AREA UTAMA: UPLOAD 2 FOTO UJI
# ==========================================
st.markdown("## 🔍 Upload Dua Wajah untuk Dibandingkan")

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 📸 Foto Pertama")
    face1_file = st.file_uploader("Upload Foto 1", type=["jpg","jpeg","png"], key="f1", label_visibility="collapsed")
with col2:
    st.markdown("#### 📸 Foto Kedua")
    face2_file = st.file_uploader("Upload Foto 2", type=["jpg","jpeg","png"], key="f2", label_visibility="collapsed")

# ==========================================
# 7. TOMBOL PROSES
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
            
            vec1, img1, det1 = preprocess_with_face_detection(face1_file.getvalue(), IMG_SIZE)
            vec2, img2, det2 = preprocess_with_face_detection(face2_file.getvalue(), IMG_SIZE)
            
            proj1 = pca.transform([vec1])
            proj2 = pca.transform([vec2])
            similarity = cosine_similarity(proj1, proj2)[0][0]
            
            progress_bar.empty()
            
            st.markdown("---")
            st.subheader("📊 Hasil Deteksi")
            
            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.image(img1, caption="Foto 1 (Resize)", width=150)
                st.markdown('</div>', unsafe_allow_html=True)
            with col_r2:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.image(img2, caption="Foto 2 (Resize)", width=150)
                st.markdown('</div>', unsafe_allow_html=True)
            with col_r3:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.metric("Skor Kemiripan", f"{similarity:.2%}")
                if similarity >= threshold:
                    st.success("✅ MIRIP")
                    st.balloons()
                else:
                    st.error("❌ TIDAK MIRIP")
                st.caption(f"Komponen PCA: {k}")
                st.caption(f"Varians: {np.sum(pca.explained_variance_ratio_)*100:.1f}%")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.subheader("📈 Grafik Akumulasi Informasi")
            explained_variance = np.cumsum(pca.explained_variance_ratio_)
            fig, ax = plt.subplots()
            ax.plot(range(1, len(explained_variance)+1), explained_variance, 'bo-')
            ax.axhline(y=0.95, color='r', linestyle='--', label='95%')
            ax.axhline(y=threshold, color='g', linestyle=':', label=f'Threshold {threshold:.2f}')
            ax.set_xlabel('Jumlah Komponen PCA (k)')
            ax.set_ylabel('Akumulasi Informasi')
            ax.legend()
            st.pyplot(fig)
