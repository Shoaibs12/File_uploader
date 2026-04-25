import os
import sqlite3
import uuid
import time
import streamlit as st
import shutil
import base64

# --- Configuration & Styling ---
st.set_page_config(page_title="FileVault - Upload System", page_icon="🗂️", layout="centered")

# Custom CSS for EXACT React clone
hide_st_style = """
<style>
    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #0a0a0f !important;
        color: #e0e0e0;
    }
    
    .stApp {
        background-color: #0a0a0f !important;
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 700 !important;
    }
    
    /* Tabs Styling */
    div[data-testid="stTabs"] {
        background: transparent;
    }
    button[data-baseweb="tab"] {
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        color: #666 !important;
        font-weight: 600 !important;
        transition: all 0.15s !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: rgba(99,102,241,0.25) !important;
        border: 1px solid rgba(99,102,241,0.4) !important;
        color: #a5b4fc !important;
    }
    div[data-baseweb="tab-highlight"] {
        display: none !important;
    }
    
    /* File Uploader Dropzone */
    [data-testid="stFileUploaderDropzone"] {
        border: 2px dashed rgba(255,255,255,0.12) !important;
        border-radius: 18px !important;
        padding: 90px 24px !important;
        background: rgba(255,255,255,0.02) !important;
        transition: all 0.2s !important;
        text-align: center !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: rgba(255,255,255,0.25) !important;
        background: rgba(99,102,241,0.08) !important;
    }
    [data-testid="stFileUploaderDropzone"] small {
        display: none !important;
    }
    
    /* Custom Centered Upload Sign */
    /* Custom Centered Upload Sign */
    [data-testid="stFileUploaderDropzone"] button {
        display: none !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] > div > span,
    [data-testid="stFileUploaderDropzoneInstructions"] > div > svg {
        display: none !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] > div {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] > div::after {
        content: "📂 \\A Drag & drop files here";
        display: block;
        white-space: pre-wrap;
        text-align: center;
        font-size: 16px;
        font-weight: 500;
        color: #888;
        line-height: 1.5;
        margin-top: 14px;
    }
    
    /* Primary Button overrides */
    button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        border: none !important;
        border-radius: 10px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px 18px !important;
    }
    
    /* Download Button (Secondary) */
    div[data-testid="stDownloadButton"] button {
        background: rgba(99,102,241,0.15) !important;
        border: 1px solid rgba(99,102,241,0.3) !important;
        color: #a5b4fc !important;
        border-radius: 8px !important;
        padding: 6px 10px !important;
        font-size: 14px !important;
        height: 38px !important;
        width: 100% !important;
    }
    div[data-testid="stDownloadButton"] button:hover {
        background: rgba(99,102,241,0.3) !important;
    }

    /* Input fields */
    .stTextInput input {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #e0e0e0 !important;
        border-radius: 10px !important;
        font-family: 'DM Mono', monospace !important;
        padding: 10px 14px !important;
    }
    
    /* File Card overrides for specific elements */
    .file-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 16px;
        display: flex;
        gap: 14px;
        align-items: center;
        margin-bottom: 10px;
        transition: background 0.2s;
    }
    .file-card:hover {
        background: rgba(255,255,255,0.07);
    }
    .file-icon {
        width: 52px; height: 52px;
        border-radius: 10px;
        background: rgba(99,102,241,0.15);
        border: 1.5px solid rgba(99,102,241,0.3);
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; font-size: 10px; color: #a5b4fc;
        letter-spacing: 0.5px;
    }
    .file-info {
        flex: 1;
        min-width: 0;
    }
    .file-name {
        font-family: 'DM Mono', monospace;
        font-size: 13px; font-weight: 600; color: #f0f0f0;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .file-meta {
        font-size: 11px; color: #888; margin-top: 3px; display: flex; gap: 10px;
    }
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Delete Button specific CSS hack (since Streamlit doesn't distinguish button types easily beyond primary/secondary)
st.markdown("""
<style>
div[data-testid="stHorizontalBlock"] > div:nth-child(3) button {
    background: rgba(239,68,68,0.1) !important;
    border: 1px solid rgba(239,68,68,0.25) !important;
    color: #f87171 !important;
    border-radius: 8px !important;
    padding: 6px 10px !important;
    font-size: 14px !important;
    height: 38px !important;
    width: 100% !important;
}
div[data-testid="stHorizontalBlock"] > div:nth-child(3) button:hover {
    background: rgba(239,68,68,0.25) !important;
}
</style>
""", unsafe_allow_html=True)

# --- Constants & Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
DB_FILE = os.path.join(BASE_DIR, "filevault.db")
MAX_SIZE_MB = 10
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Database Integration ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            size INTEGER NOT NULL,
            uploadedAt INTEGER NOT NULL,
            filepath TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# --- Helper Functions ---
def format_bytes(bytes_val):
    if bytes_val < 1024: return f"{bytes_val} B"
    if bytes_val < 1024 * 1024: return f"{(bytes_val / 1024):.1f} KB"
    return f"{(bytes_val / (1024 * 1024)):.2f} MB"

def format_date(ts):
    from datetime import datetime
    return datetime.fromtimestamp(ts / 1000).strftime('%d %b %Y, %H:%M')

def save_uploaded_file(uploaded_file):
    if uploaded_file.size > MAX_SIZE_BYTES:
        return False, f"File exceeds {MAX_SIZE_MB}MB limit."
        
    file_id = str(uuid.uuid4())[:8]
    filepath = os.path.join(UPLOAD_DIR, f"{file_id}_{uploaded_file.name}")
    
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    size = os.path.getsize(filepath)
    uploadedAt = int(time.time() * 1000)
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO files (id, name, type, size, uploadedAt, filepath) VALUES (?, ?, ?, ?, ?, ?)",
        (file_id, uploaded_file.name, uploaded_file.type, size, uploadedAt, filepath)
    )
    conn.commit()
    conn.close()
    
    return True, "File uploaded successfully."

def delete_file(file_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM files WHERE id = ?", (file_id,))
    row = cursor.fetchone()
    
    if row:
        filepath = row["filepath"]
        if os.path.exists(filepath):
            os.remove(filepath)
        cursor.execute("DELETE FROM files WHERE id = ?", (file_id,))
        conn.commit()
    conn.close()

# --- Fetch Data ---
conn = get_db()
files = conn.execute("SELECT * FROM files ORDER BY uploadedAt DESC").fetchall()
conn.close()
total_size = sum(f["size"] for f in files)

# --- App UI (HTML Injection) ---

# Header & Stats Box
header_html = f"""
<div style="display: flex; align-items: center; gap: 14px; margin-bottom: 8px; margin-top: 20px;">
    <div style="width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(135deg, #6366f1, #8b5cf6); display: flex; align-items: center; justify-content: center; font-size: 20px; box-shadow: 0 4px 16px rgba(99,102,241,0.4);">
        ⬆
    </div>
    <div>
        <h1 style="margin: 0; font-size: 26px; font-weight: 700; letter-spacing: -0.5px; color: #fff;">FileVault</h1>
        <p style="margin: 0; font-size: 12px; color: #666; font-family: 'DM Mono', monospace;">Secure • Validated • Tracked</p>
    </div>
</div>

<div style="display: flex; gap: 20px; margin-top: 20px; margin-bottom: 20px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 12px; padding: 14px 20px;">
    <div style="flex: 1;">
        <div style="font-size: 18px; font-weight: 700; color: #fff; font-family: 'DM Mono', monospace;">{len(files)}</div>
        <div style="font-size: 11px; color: #666; margin-top: 2px;">Files Stored</div>
    </div>
    <div style="flex: 1;">
        <div style="font-size: 18px; font-weight: 700; color: #fff; font-family: 'DM Mono', monospace;">{format_bytes(total_size)}</div>
        <div style="font-size: 11px; color: #666; margin-top: 2px;">Total Size</div>
    </div>
    <div style="flex: 1;">
        <div style="font-size: 18px; font-weight: 700; color: #fff; font-family: 'DM Mono', monospace;">{MAX_SIZE_MB} MB</div>
        <div style="font-size: 11px; color: #666; margin-top: 2px;">Max File Size</div>
    </div>
    <div style="flex: 1;">
        <div style="font-size: 18px; font-weight: 700; color: #fff; font-family: 'DM Mono', monospace;">Python</div>
        <div style="font-size: 11px; color: #666; margin-top: 2px;">Stack</div>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["Upload", f"Library ({len(files)})"])

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 1

with tab1:
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload", 
        accept_multiple_files=True,
        type=["jpg", "png", "gif", "webp", "pdf", "txt", "json", "csv", "zip", "mp4", "doc", "docx"],
        key=str(st.session_state.uploader_key),
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='text-align: center; font-size: 12px; color: #888; font-family: monospace; margin-top: -10px; margin-bottom: 20px;'>Allowed types: JPG, PNG, GIF, WEBP, PDF, TXT, JSON, CSV, ZIP, MP4, DOC, DOCX<br>Maximum file size: 10 MB per file</div>", unsafe_allow_html=True)
    
    invalid_files = []
    if uploaded_files:
        for uf in uploaded_files:
            if uf.size > MAX_SIZE_BYTES:
                invalid_files.append(uf)
                st.error(f"⚠️ **{uf.name}** is {format_bytes(uf.size)}, which exceeds the 10 MB limit.")
    
    if st.button("Upload Files", type="primary", use_container_width=True, disabled=len(invalid_files) > 0):
        if uploaded_files:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, uf in enumerate(uploaded_files):
                status_text.markdown(f"<span style='color: #a5b4fc; font-size: 14px;'>Uploading {uf.name}...</span>", unsafe_allow_html=True)
                success, msg = save_uploaded_file(uf)
                if not success:
                    st.warning(f"⚠️ {msg}")
                else:
                    pass
                progress_bar.progress((i + 1) / len(uploaded_files))
                time.sleep(0.1)
                
            status_text.markdown("<span style='color: #4ade80; font-size: 14px;'>✓ All uploads complete!</span>", unsafe_allow_html=True)
            time.sleep(1)
            st.session_state.uploader_key += 1
            st.rerun()

with tab2:
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    search_term = st.text_input("", placeholder="Search files...", label_visibility="collapsed")
    
    filtered_files = [f for f in files if search_term.lower() in f["name"].lower()]
    
    if not filtered_files:
        st.markdown("""
        <div style="text-align: center; padding: 60px 24px; background: rgba(255,255,255,0.02); border-radius: 16px; border: 1px dashed rgba(255,255,255,0.07);">
            <div style="font-size: 40px; margin-bottom: 12px;">📭</div>
            <div style="color: #555; font-size: 14px;">No files found.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
        for f in filtered_files:
            # We use an outer container to wrap the custom HTML and Streamlit buttons together
            with st.container():
                # To perfectly align the card, we render the background in HTML and place buttons inside Streamlit columns over it? No, Streamlit columns can't overlay.
                # So we render the left part of the card, and use columns to put the buttons next to it.
                # We style the stHorizontalBlock to look like the file card!
                
                col1, col2, col3 = st.columns([6, 1, 1])
                
                ext = f['type'].split('/')[-1].upper()[:4]
                if not ext or ext == 'OCTE': ext = 'FILE'
                
                file_html = f"""
                <div style="display: flex; gap: 14px; align-items: center; padding: 4px 0;">
                    <div class="file-icon">{ext}</div>
                    <div class="file-info">
                        <div class="file-name">{f['name']}</div>
                        <div class="file-meta">
                            <span style="color: #a5b4fc; font-weight: 600;">{ext}</span>
                            <span>{format_bytes(f['size'])}</span>
                            <span>{format_date(f['uploadedAt'])}</span>
                        </div>
                    </div>
                </div>
                """
                col1.markdown(file_html, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                    with open(f["filepath"], "rb") as file_data:
                        st.download_button(label="↓", data=file_data, file_name=f["name"], key=f"dl_{f['id']}")
                with col3:
                    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                    if st.button("✕", key=f"del_{f['id']}"):
                        delete_file(f['id'])
                        st.rerun()
                
                st.markdown("<hr style='margin: 4px 0 16px 0; border: none; border-top: 1px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
