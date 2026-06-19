# app.py - VERSI SEDERHANA (Tombol Sakura di 2 Tempat)
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

# --- CSS sederhana ---
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #FFF0F5, #FFE4E9, #FCE4EC);
        }
        .main-title {
            text-align: center;
            color: #AD1457;
            font-size: 42px;
            font-weight: bold;
        }
        .sub-title {
            text-align: center;
            color: #D81B60;
            font-size: 18px;
        }
        .result-card {
            background: #FCE4EC;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid #F8BBD0;
        }
        .sakura-btn {
            font-size: 32px;
            background: transparent;
            border: 2px solid #EC407A;
            border-radius: 50%;
            padding: 8px 14px;
            cursor: pointer;
            transition: 0.3s;
        }
        .sakura-btn:hover {
            transform: scale(1.1) rotate(15deg);
            background: rgba(236,64,122,0.2);
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
# 4. JUDUL + TOMBOL SAKURA DI MAIN AREA
# ==========================================
col_title, col_toggle = st.columns([6, 1])
with col_title:
    st.markdown('<p class="main-title">🌸 Deteksi Kemiripan Wajah</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Menggunakan PCA (Eigenfaces) & Cosine Similarity</p>', unsafe_allow_html=True)
with col_toggle:
    # Tombol sakura di pojok kanan atas (backup)
    if st.button("🌸", key="toggle_main"):
        st.session_state.show_upload = not st.session_state.show_upload
        st.rerun()
    st.caption("Toggle")

# ==========================================
# 5. SIDEBAR (dengan tombol sakura di atas)
# ==========================================
with st.sidebar:
    st.markdown("---")
    # Tombol sakura di sidebar
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌸", key="toggle_sidebar"):
            st.session_state.show_upload = not st.session_state.show_upload
            st.rerun()
        st.caption("Klik Sakura")
    st.markdown("---")
    
    # Logo
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    
    # === UPLOAD DATA LATIH (toggle) ===
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
        st.info("🌸 Upload disembunyikan. Klik sakura di atas atau di pojok kanan atas.")
    
    st.divider()
    
    # Threshold
    threshold = st.slider("🎯 Ambang Batas Kemiripan", 0.0, 1.0, 0.70, 0.05)
    st.caption(f"Threshold: {threshold:.2f}")
    
    st.divider()
    
    # Anggota
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
st.header("🔍 Upload Dua Wajah untuk Dibandingkan")

col1, col2 = st.columns(2)
with col1:
    face1_file = st.file_uploader("Foto 1", type=["jpg","jpeg","png"], key="f1")
with col2:
    face2_file = st.file_uploader("Foto 2", type=["jpg","jpeg","png"], key="f2")

# ==========================================
# 7. TOMBOL PROSES
# ==========================================
if st.button("🚀 Proses Deteksi Sekarang", use_container_width=True):
    # Cek apakah uploaded_train_files ada
    if 'uploaded_train_files' not in locals() or not uploaded_train_files or len(uploaded_train_files) < 10:
        st.error("⚠️ **Data Latih Kurang!** Upload minimal 10 foto.")
        st.info("💡 Klik tombol 🌸 di sidebar atau pojok kanan atas untuk menampilkan bagian upload.")
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
            
            # Tampilkan hasil
            st.markdown("---")
            st.subheader("📊 Hasil Deteksi")
            
            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.image(img1, caption="Foto 1 (Resize)", width=150)
            with col_r2:
                st.image(img2, caption="Foto 2 (Resize)", width=150)
            with col_r3:
                st.metric("Skor Kemiripan", f"{similarity:.2%}")
                if similarity >= threshold:
                    st.success("✅ MIRIP")
                    st.balloons()
                else:
                    st.error("❌ TIDAK MIRIP")
                st.caption(f"Komponen PCA: {k}")
                st.caption(f"Varians: {np.sum(pca.explained_variance_ratio_)*100:.1f}%")
            
            # Grafik
            st.subheader("📈 Grafik Akumulasi Informasi")
            explained_variance = np.cumsum(pca.explained_variance_ratio_)
            fig, ax = plt.subplots()
            ax.plot(range(1, len(explained_variance)+1), explained_variance, 'bo-')
            ax.axhline(y=0.95, color='r', linestyle='--', label='95%')
            ax.axhline(y=threshold, color='g', linestyle=':', label=f'Threshold {threshold:.2f}')
            ax.set_xlabel('k')
            ax.set_ylabel('Akumulasi Informasi')
            ax.legend()
            st.pyplot(fig)
