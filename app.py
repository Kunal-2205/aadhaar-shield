import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os
import numpy as np

# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────
API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="Aadhaar Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ──────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root & Background ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #0a0d14;
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: #0f1420; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Main wrapper ── */
.main .block-container {
    padding: 2rem 3rem 4rem;
    max-width: 1200px;
}

/* ── Hero banner ── */
.hero {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #1e2535;
}
.hero-icon {
    font-size: 2.6rem;
    line-height: 1;
}
.hero-title {
    font-size: 2rem;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: -0.03em;
    margin: 0;
}
.hero-sub {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0.15rem 0 0;
    font-weight: 400;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.hero-badge {
    margin-left: auto;
    background: #0f2a1a;
    border: 1px solid #15803d;
    color: #4ade80;
    font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
    padding: 0.3rem 0.8rem;
    border-radius: 99px;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── Step labels ── */
.step-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.6rem;
}
.step-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #cbd5e1;
    margin-bottom: 1.2rem;
}

/* ── Upload zone ── */
[data-testid="stFileUploader"] {
    background: #0f1420 !important;
    border: 2px dashed #1e2d45 !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #3b82f6 !important;
}
[data-testid="stFileUploader"] label {
    color: #64748b !important;
    font-size: 0.85rem !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #3b82f6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.02em !important;
    padding: 0.55rem 1.4rem !important;
    transition: opacity 0.15s, transform 0.1s !important;
    width: 100%;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Detection cards ── */
.det-card {
    background: #0f1420;
    border: 1px solid #1e2535;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.85rem;
    transition: border-color 0.15s;
}
.det-card:hover { border-color: #3b82f6; }
.det-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
}
.det-label {
    font-size: 0.82rem;
    font-weight: 600;
    color: #e2e8f0;
    flex: 1;
}
.det-class {
    font-size: 0.72rem;
    color: #475569;
    font-family: 'JetBrains Mono', monospace;
}
.det-conf {
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    color: #4ade80;
    background: #0f2a1a;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
}

/* ── Section divider ── */
.divider {
    border: none;
    border-top: 1px solid #1e2535;
    margin: 1.8rem 0;
}

/* ── Mask type pills ── */
.stRadio > div {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}
.stRadio label {
    background: #0f1420 !important;
    border: 1px solid #1e2535 !important;
    border-radius: 8px !important;
    padding: 0.4rem 1rem !important;
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
    cursor: pointer !important;
    transition: all 0.15s !important;
}
.stRadio label:hover {
    border-color: #3b82f6 !important;
    color: #e2e8f0 !important;
}
[data-testid="stRadio"] [aria-checked="true"] + label,
.stRadio [data-checked="true"] {
    border-color: #3b82f6 !important;
    color: #fff !important;
    background: #1e3a5f !important;
}

/* ── Checkbox ── */
.stCheckbox label {
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
}

/* ── Image display ── */
[data-testid="stImage"] img {
    border-radius: 10px;
    border: 1px solid #1e2535;
    width: 100%;
}

/* ── Info / alert pills ── */
.info-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #0c1929;
    border: 1px solid #1e3a5f;
    color: #93c5fd;
    font-size: 0.75rem;
    padding: 0.3rem 0.75rem;
    border-radius: 6px;
    margin-bottom: 1rem;
    font-family: 'JetBrains Mono', monospace;
}
.warn-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #1c1000;
    border: 1px solid #78350f;
    color: #fbbf24;
    font-size: 0.75rem;
    padding: 0.3rem 0.75rem;
    border-radius: 6px;
    margin-bottom: 1rem;
    font-family: 'JetBrains Mono', monospace;
}
.success-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #0f2a1a;
    border: 1px solid #15803d;
    color: #4ade80;
    font-size: 0.75rem;
    padding: 0.3rem 0.75rem;
    border-radius: 6px;
    margin-bottom: 1rem;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Download button ── */
.dl-btn {
    display: inline-block;
    background: linear-gradient(135deg, #15803d, #16a34a);
    color: #fff !important;
    border-radius: 8px;
    padding: 0.55rem 1.4rem;
    font-weight: 600;
    font-size: 0.85rem;
    text-decoration: none;
    text-align: center;
    width: 100%;
    box-sizing: border-box;
    margin-top: 0.5rem;
    transition: opacity 0.15s;
}
.dl-btn:hover { opacity: 0.85; }

/* ── Column gap ── */
[data-testid="column"] { padding: 0 0.8rem; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────
for k, v in {
    "image_id": None,
    "detections": [],
    "preview_bytes": None,
    "masked_bytes": None,
    "uploaded_bytes": None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
CLASS_COLORS = {
    "Aadhaar Back Side": "#5b8ac6",
    "Aadhaar Barcode": "#3cb4dc",
    "Aadhaar Emblem": "#8c5ac8",
    "Aadhaar Front Side": "#4ade80",
    "Government of India Text": "#c8c800",
    "Masked Aadhaar Region": "#5a5a5a",
    "Aadhaar Number": "#fb923c",
    "Photo": "#ff8000",
    "QR Code": "#e879f9",
    "Aadhaar Top Section": "#00c8c8",
    "UIDAI Logo/Text": "#60a5fa",
    "Virtual ID (VID)": "#64ff64",
    "Passport Card": "#dc3232",
    "Voter ID Card": "#dc32dc",
    "Passport Emblem": "#965a64",
    "Passport Front Side": "#ffa500",
    "Passport Govt Text": "#aaaa00",
    "Passport Number": "#960000",
}

MASK_ICONS = {"black": "⬛", "blur": "🌫️", "pixelate": "🟦"}


def img_to_b64(data: bytes) -> str:
    return base64.b64encode(data).decode()


def draw_preview(img_bytes: bytes, detections: list) -> bytes:
    """Fallback: draw bounding boxes with Pillow if disk preview not found."""
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    draw = ImageDraw.Draw(img)
    color_map = {
        "Aadhaar Back Side": "#5b8ac6",
        "Aadhaar Barcode": "#3cb4dc",
        "Aadhaar Emblem": "#8c5ac8",
        "Aadhaar Front Side": "#4ade80",
        "Government of India Text": "#c8c800",
        "Masked Aadhaar Region": "#5a5a5a",
        "Aadhaar Number": "#fb923c",
        "Photo": "#ff8000",
        "QR Code": "#e879f9",
        "Aadhaar Top Section": "#00c8c8",
        "UIDAI Logo/Text": "#60a5fa",
        "Virtual ID (VID)": "#64ff64",
        "Passport Card": "#dc3232",
        "Voter ID Card": "#dc32dc",
        "Passport Emblem": "#965a64",
        "Passport Front Side": "#ffa500",
        "Passport Govt Text": "#aaaa00",
        "Passport Number": "#960000",
    }
    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        color = color_map.get(det["class"], "#ffffff")
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
        label = f"#{det['id']} {det['class']} {int(det['confidence']*100)}%"
        lw = len(label) * 7
        draw.rectangle([x1, max(y1 - 20, 0), x1 + lw, y1], fill=color)
        draw.text((x1 + 2, max(y1 - 18, 0)), label, fill="#000000")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=92)
    return buf.getvalue()


# ──────────────────────────────────────────────
# HERO
# ──────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-icon">🛡️</div>
  <div>
    <p class="hero-title">Aadhaar Shield</p>
    <p class="hero-sub">AI-powered PII Detection &amp; Masking</p>
  </div>
  <span class="hero-badge">YOLOv8 · FastAPI</span>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# LAYOUT  — left panel | right panel
# ──────────────────────────────────────────────
left, right = st.columns([1, 1.35], gap="large")

# ════════════════════════════════════════════
# LEFT PANEL  —  Upload + Detect
# ════════════════════════════════════════════
with left:
    st.markdown('<p class="step-label">Step 1</p><p class="step-title">Upload Aadhaar Image</p>', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop a JPG / PNG of your Aadhaar card",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded:
        st.session_state.uploaded_bytes = uploaded.read()
        st.image(st.session_state.uploaded_bytes, use_container_width=True, caption="Uploaded image")

    detect_clicked = st.button("🔍  Detect Fields", disabled=uploaded is None)

    if detect_clicked and uploaded:
        with st.spinner("Running YOLOv8 detection…"):
            try:
                files = {"file": (uploaded.name, st.session_state.uploaded_bytes, uploaded.type)}
                resp = requests.post(f"{API_BASE}/detect/", files=files, timeout=30)
                resp.raise_for_status()
                data = resp.json()

                st.session_state.image_id   = data["image_id"]
                st.session_state.detections = data["detections"]
                st.session_state.masked_bytes = None  # reset old mask

                # Read preview image directly from disk (same machine as API)
                image_id = data["image_id"]
                ext = os.path.splitext(uploaded.name)[1]  # e.g. .jpg or .png
                preview_path = os.path.join("uploads", "previews", image_id + ext)
                # Fallback: also try .jpg if original ext not found
                if not os.path.exists(preview_path):
                    preview_path = os.path.join("uploads", "previews", image_id + ".jpg")
                if os.path.exists(preview_path):
                    with open(preview_path, "rb") as pf:
                        st.session_state.preview_bytes = pf.read()
                else:
                    # Fallback: draw boxes client-side with Pillow
                    st.session_state.preview_bytes = draw_preview(
                        st.session_state.uploaded_bytes,
                        data["detections"]
                    )

            except requests.exceptions.ConnectionError:
                st.markdown('<div class="warn-pill">⚠ Cannot reach API at ' + API_BASE + ' — is the server running?</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Detection failed: {e}")

    # ── Detection results ──
    if st.session_state.detections:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown(f'<p class="step-label">Detected Fields — {len(st.session_state.detections)} found</p>', unsafe_allow_html=True)

        for det in st.session_state.detections:
            color = CLASS_COLORS.get(det["class"], "#94a3b8")
            conf_pct = int(det["confidence"] * 100)
            st.markdown(f"""
            <div class="det-card">
              <div class="det-dot" style="background:{color};box-shadow:0 0 6px {color}66;"></div>
              <div style="flex:1">
                <div class="det-label">#{det['id']} · {det['class']}</div>
                <div class="det-class">bbox [{det['bbox'][0]}, {det['bbox'][1]}, {det['bbox'][2]}, {det['bbox'][3]}]</div>
              </div>
              <span class="det-conf">{conf_pct}%</span>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════
# RIGHT PANEL  —  Preview + Mask
# ════════════════════════════════════════════
with right:
    st.markdown('<p class="step-label">Step 2</p><p class="step-title">Preview &amp; Mask</p>', unsafe_allow_html=True)

    if st.session_state.preview_bytes:
        st.image(st.session_state.preview_bytes, use_container_width=True, caption="Detection preview")
    elif not st.session_state.detections:
        st.markdown("""
        <div style="background:#0f1420;border:1px dashed #1e2535;border-radius:12px;
                    height:220px;display:flex;align-items:center;justify-content:center;
                    color:#334155;font-size:0.85rem;">
          Preview appears after detection
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.detections:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<p class="step-label">Step 3 — Choose fields to mask</p>', unsafe_allow_html=True)

        # ── Field checkboxes ──
        selected_ids = []
        cols = st.columns(2)
        for i, det in enumerate(st.session_state.detections):
            col = cols[i % 2]
            color = CLASS_COLORS.get(det["class"], "#94a3b8")
            checked = col.checkbox(
                f"#{det['id']} {det['class']}",
                value=True,
                key=f"chk_{det['id']}"
            )
            if checked:
                selected_ids.append(det["id"])

        st.markdown('<p class="step-label" style="margin-top:1.2rem;">Masking style</p>', unsafe_allow_html=True)
        mask_type = st.radio(
            "mask_style",
            options=["black", "blur", "pixelate"],
            format_func=lambda x: f"{MASK_ICONS[x]}  {x.capitalize()}",
            horizontal=True,
            label_visibility="collapsed"
        )

        mask_clicked = st.button("🛡️  Apply Mask", disabled=not selected_ids)

        if mask_clicked and selected_ids:
            with st.spinner("Applying mask…"):
                try:
                    payload = {
                        "image_id": st.session_state.image_id,
                        "selected_ids": selected_ids,
                        "mask_type": mask_type
                    }
                    resp = requests.post(f"{API_BASE}/mask/", json=payload, timeout=30)
                    resp.raise_for_status()
                    st.session_state.masked_bytes = resp.content
                except requests.exceptions.ConnectionError:
                    st.markdown('<div class="warn-pill">⚠ Cannot reach API — is the server running?</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Masking failed: {e}")

    # ── Masked result ──
    if st.session_state.masked_bytes:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="success-pill">✓ Masking complete</div>', unsafe_allow_html=True)
        st.image(st.session_state.masked_bytes, use_container_width=True, caption="Masked output")

        b64 = img_to_b64(st.session_state.masked_bytes)
        st.markdown(
            f'<a class="dl-btn" href="data:image/jpeg;base64,{b64}" download="masked_aadhaar.jpg">⬇  Download Masked Image</a>',
            unsafe_allow_html=True
        )

# ──────────────────────────────────────────────
# RESET
# ──────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
if st.button("↺  Start Over", key="reset"):
    for k in ["image_id", "detections", "preview_bytes", "masked_bytes", "uploaded_bytes"]:
        st.session_state[k] = None if k != "detections" else []
    st.rerun()