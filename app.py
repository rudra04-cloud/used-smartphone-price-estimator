import joblib
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Used Smartphone Resell Price Estimator",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------
# Custom CSS: Glassmorphism, Cursor Reactivity & Smooth Keyframe Motion
# --------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --accent: #6366f1;
    --emerald: #059669;
    --emerald-light: #10b981;
    --surface: rgba(255, 255, 255, 0.88);
    --border-subtle: rgba(148, 163, 184, 0.28);
    --text-main: #0f172a;
    --text-muted: #475569;
    --ease-spring: cubic-bezier(0.22, 1, 0.36, 1);
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Ambient Mesh Background */
.stApp {
    background:
        radial-gradient(at 0% 0%, rgba(37, 99, 235, 0.08) 0px, transparent 48%),
        radial-gradient(at 100% 0%, rgba(99, 102, 241, 0.08) 0px, transparent 45%),
        radial-gradient(at 85% 95%, rgba(16, 185, 129, 0.06) 0px, transparent 50%),
        #f8fafc;
}

/* Entrance Keyframes */
@keyframes fadeSlideUp {
    0% {
        opacity: 0;
        transform: translateY(18px) scale(0.985);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes pulseDot {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.45); opacity: 0.55; }
}

@keyframes growProgress {
    from { width: 0%; }
}

@keyframes shimmerSweep {
    0% { transform: translateX(-100%) skewX(-18deg); }
    100% { transform: translateX(250%) skewX(-18deg); }
}

/* Hero Banner with Animated Gradient & Cursor Spotlight */
.hero-banner {
    position: relative;
    overflow: hidden;
    background: linear-gradient(125deg, #090d16 0%, #172554 42%, #1d4ed8 78%, #3b82f6 100%);
    background-size: 200% 200%;
    animation: fadeSlideUp 0.65s var(--ease-spring) both, gradientFlow 12s ease infinite;
    padding: 2.15rem 2.4rem;
    border-radius: 22px;
    color: #ffffff;
    margin-bottom: 1.35rem;
    box-shadow: 0 18px 40px -12px rgba(29, 78, 216, 0.35);
    border: 1px solid rgba(255, 255, 255, 0.16);
    transition: transform 0.35s var(--ease-spring), box-shadow 0.35s var(--ease-spring);
}

.hero-banner::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(
        480px circle at var(--mouse-x, 50%) var(--mouse-y, 50%),
        rgba(255, 255, 255, 0.14),
        transparent 70%
    );
    opacity: 0;
    transition: opacity 0.35s ease;
    pointer-events: none;
}

.hero-banner:hover::before {
    opacity: 1;
}

.hero-banner:hover {
    transform: translateY(-2px);
    box-shadow: 0 22px 46px -12px rgba(29, 78, 216, 0.44);
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(8px);
    color: #dbeafe;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    border: 1px solid rgba(255, 255, 255, 0.18);
    margin-bottom: 0.8rem;
}

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #34d399;
    display: inline-block;
    animation: pulseDot 2s infinite ease-in-out;
}

.hero-title {
    font-size: 2.05rem;
    font-weight: 800;
    margin: 0 0 0.4rem 0;
    line-height: 1.18;
    letter-spacing: -0.025em;
}

.hero-subtitle {
    font-size: 0.98rem;
    color: #cbd5e1;
    margin: 0;
    max-width: 740px;
    line-height: 1.55;
}

/* Reactive Specification Cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    position: relative;
    background: var(--surface) !important;
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-subtle) !important;
    border-radius: 18px !important;
    padding: 0.35rem 0.25rem;
    box-shadow: 0 4px 20px -4px rgba(15, 23, 42, 0.05);
    transition:
        transform 0.35s var(--ease-spring),
        box-shadow 0.35s var(--ease-spring),
        border-color 0.3s ease,
        background-color 0.3s ease;
    animation: fadeSlideUp 0.65s var(--ease-spring) both;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-5px);
    border-color: rgba(37, 99, 235, 0.48) !important;
    background: #ffffff !important;
    box-shadow:
        0 20px 32px -12px rgba(37, 99, 235, 0.14),
        0 4px 12px -2px rgba(15, 23, 42, 0.05);
}

[data-testid="stVerticalBlockBorderWrapper"]:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.14), 0 16px 28px -10px rgba(37, 99, 235, 0.16);
}

/* Section Card Headers */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding-bottom: 0.7rem;
    margin-bottom: 0.9rem;
    border-bottom: 1px solid #e2e8f0;
}

.section-icon {
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    color: #2563eb;
    width: 36px;
    height: 36px;
    border-radius: 11px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 1.15rem;
    transition: transform 0.35s var(--ease-spring);
}

[data-testid="stVerticalBlockBorderWrapper"]:hover .section-icon {
    transform: scale(1.1) rotate(-4deg);
}

.section-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-main);
    margin: 0;
}

/* Smooth Input Hover Transitions */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    border-radius: 11px !important;
    transition: border-color 0.22s ease, box-shadow 0.22s ease, transform 0.2s ease !important;
}

div[data-baseweb="select"] > div:hover,
div[data-baseweb="input"] > div:hover {
    border-color: #3b82f6 !important;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.08) !important;
}

/* Live Conversion Pill */
.conversion-pill {
    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
    border: 1px solid #cbd5e1;
    border-radius: 11px;
    padding: 0.65rem 0.9rem;
    font-size: 0.84rem;
    color: #334155;
    margin-top: 0.45rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: transform 0.25s var(--ease-spring), border-color 0.25s ease;
}

.conversion-pill:hover {
    transform: scale(1.015);
    border-color: #3b82f6;
}

.conversion-pill strong {
    color: #0f172a;
}

/* Secondary Preset Buttons */
div.stButton > button[kind="secondary"] {
    background: #ffffff;
    color: #1e293b;
    border: 1px solid #cbd5e1;
    border-radius: 999px;
    font-size: 0.83rem;
    font-weight: 600;
    padding: 0.4rem 1rem;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
    transition: all 0.25s var(--ease-spring);
}

div.stButton > button[kind="secondary"]:hover {
    border-color: #2563eb;
    color: #2563eb;
    background: #eff6ff;
    transform: translateY(-2px);
    box-shadow: 0 6px 14px -4px rgba(37, 99, 235, 0.22);
}

/* Primary Shimmering Gradient CTA Button */
div.stButton > button[kind="primary"] {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
    color: #ffffff;
    font-weight: 700;
    font-size: 1.02rem;
    letter-spacing: 0.01em;
    padding: 0.82rem 1.6rem;
    border-radius: 14px;
    border: none;
    box-shadow: 0 10px 24px -6px rgba(37, 99, 235, 0.48);
    transition: transform 0.3s var(--ease-spring), box-shadow 0.3s var(--ease-spring);
}

div.stButton > button[kind="primary"]::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 45%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.28), transparent);
    transform: translateX(-120%) skewX(-18deg);
}

div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) scale(1.005);
    box-shadow: 0 16px 30px -6px rgba(79, 70, 229, 0.55);
    color: #ffffff;
}

div.stButton > button[kind="primary"]:hover::after {
    animation: shimmerSweep 0.85s ease forwards;
}

div.stButton > button[kind="primary"]:active {
    transform: translateY(0px) scale(0.985);
}

/* Ready Prompt Placeholder */
.ready-banner {
    background: rgba(255, 255, 255, 0.72);
    border: 1px dashed #cbd5e1;
    border-radius: 16px;
    padding: 1.1rem 1.5rem;
    text-align: center;
    color: #475569;
    font-size: 0.92rem;
    margin-top: 0.5rem;
}

/* Valuation Output KPI Cards */
.metric-card-primary {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #047857 0%, #059669 50%, #10b981 100%);
    color: #ffffff;
    padding: 1.5rem 1.65rem;
    border-radius: 18px;
    box-shadow: 0 14px 30px -8px rgba(5, 150, 105, 0.42);
    border: 1px solid rgba(255, 255, 255, 0.2);
    animation: fadeSlideUp 0.5s var(--ease-spring) both;
    transition: transform 0.35s var(--ease-spring), box-shadow 0.35s var(--ease-spring);
}

.metric-card-primary:hover {
    transform: translateY(-5px) scale(1.01);
    box-shadow: 0 20px 36px -8px rgba(5, 150, 105, 0.52);
}

.metric-card-secondary {
    position: relative;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.94);
    color: var(--text-main);
    padding: 1.5rem 1.65rem;
    border-radius: 18px;
    border: 1px solid var(--border-subtle);
    box-shadow: 0 8px 22px -6px rgba(15, 23, 42, 0.06);
    animation: fadeSlideUp 0.6s var(--ease-spring) both;
    transition: transform 0.35s var(--ease-spring), box-shadow 0.35s var(--ease-spring), border-color 0.3s ease;
}

.metric-card-secondary:hover {
    transform: translateY(-5px) scale(1.01);
    border-color: rgba(37, 99, 235, 0.45);
    box-shadow: 0 16px 30px -8px rgba(37, 99, 235, 0.14);
}

.metric-label {
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    opacity: 0.86;
    margin-bottom: 0.4rem;
}

.metric-value {
    font-size: 1.95rem;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 0.3rem;
    letter-spacing: -0.02em;
}

.metric-sub {
    font-size: 0.83rem;
    opacity: 0.9;
}

/* Custom Animated Retention Bar */
.retention-track {
    width: 100%;
    height: 12px;
    background: #e2e8f0;
    border-radius: 999px;
    overflow: hidden;
    margin: 0.65rem 0 0.55rem 0;
}

.retention-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #2563eb 0%, #10b981 100%);
    animation: growProgress 0.9s var(--ease-spring) both;
    transition: width 0.55s var(--ease-spring);
}

/* Sidebar Cards */
.sidebar-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
    font-size: 0.88rem;
    color: #334155;
    line-height: 1.7;
    box-shadow: 0 4px 12px -4px rgba(15, 23, 42, 0.05);
    transition: transform 0.25s var(--ease-spring), border-color 0.25s ease;
}

.sidebar-card:hover {
    transform: translateY(-2px);
    border-color: #93c5fd;
}

.sidebar-card b {
    color: #0f172a;
}
</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------
# Cursor-Tracking Spotlight Script
# --------------------------------------------------------------------
components.html(
    """
    <script>
    (function() {
        try {
            const doc = window.parent.document;
            if (doc.__cursorSpotlightAttached) return;
            doc.__cursorSpotlightAttached = true;

            doc.addEventListener('pointermove', function(e) {
                const targets = doc.querySelectorAll(
                    '.hero-banner, [data-testid="stVerticalBlockBorderWrapper"], .metric-card-primary, .metric-card-secondary'
                );
                targets.forEach(function(el) {
                    const rect = el.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    el.style.setProperty('--mouse-x', x + 'px');
                    el.style.setProperty('--mouse-y', y + 'px');
                });
            }, { passive: true });
        } catch (err) {}
    })();
    </script>
    """,
    height=0,
)

# --------------------------------------------------------------------
# Load Model Pipeline
# --------------------------------------------------------------------
@st.cache_resource
def load_model():
    return joblib.load("best_phone_price_pipeline.joblib")


try:
    model = load_model()
except FileNotFoundError:
    st.error(
        "Model file `best_phone_price_pipeline.joblib` was not found in the current directory. "
        "Please re-run Cells 2–5 of `ML_Project.ipynb` to generate it."
    )
    st.stop()

# --------------------------------------------------------------------
# Session State Initialization & Presets
# --------------------------------------------------------------------
BRANDS = [
    "Samsung", "Apple", "OnePlus", "Xiaomi", "Realme", "Vivo",
    "Oppo", "Google", "Motorola", "Nokia", "Huawei", "Honor",
    "Asus", "Sony", "LG", "Lenovo", "ZTE", "HTC", "Micromax",
    "Lava", "Gionee", "Meizu", "Alcatel", "Panasonic", "Acer",
    "XOLO", "Karbonn", "Intex", "Spice", "Celkon", "Others",
]
OS_LIST = ["Android", "iOS", "Windows", "Others"]

DEFAULTS = {
    "device_brand": "Samsung",
    "os_name": "Android",
    "release_year": 2020,
    "support_5g": "no",
    "screen_size": 15.30,
    "ram": 6.0,
    "internal_memory": 128.0,
    "battery": 4500,
    "rear_camera_mp": 16.0,
    "front_camera_mp": 8.0,
    "launch_price_inr": 25000,
}

for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val


def apply_preset(preset: dict):
    for k, v in preset.items():
        st.session_state[k] = v


# --------------------------------------------------------------------
# Sidebar Specifications
# --------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📌 Project Specifications")
    st.markdown(
        """
<div class="sidebar-card">
<div><b>Institution:</b> Bennett University</div>
<div><b>Specialization:</b> B.Tech CSE (AI)</div>
<div><b>Model:</b> Random Forest (200 Trees)</div>
<div><b>Features:</b> 11 Core Attributes</div>
<div><b>Base Currency:</b> INR (₹) / USD ($)</div>
<div><b>Evaluation Split:</b> 80/20 (seed=42)</div>
</div>
""",
        unsafe_allow_html=True,
    )

    inr_per_usd = st.number_input(
        "USD → INR Exchange Rate (₹)",
        min_value=50.0,
        max_value=150.0,
        value=83.50,
        step=0.25,
        format="%.2f",
    )

    st.info(
        "**Academic Prototype Notice:** Estimates are model-derived from tabular data "
        "using non-linear tree ensembles. They represent statistical valuations, not "
        "binding market quotes."
    )

# --------------------------------------------------------------------
# Hero Header
# --------------------------------------------------------------------
st.markdown(
    """
<div class="hero-banner">
<div class="hero-badge"><span class="status-dot"></span> AI Valuation Engine • Random Forest Regressor</div>
<h1 class="hero-title">📱 Used Smartphone Resell Price Estimator</h1>
<p class="hero-subtitle">
Configure device hardware specifications or load a preset below, then click <b>Calculate Resale Valuation</b> to estimate secondary market value.
</p>
</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------
# Quick Preset Chips
# --------------------------------------------------------------------
p_label, p1, p2, p3, p4 = st.columns([1.3, 1, 1, 1, 1], gap="small")
with p_label:
    st.markdown(
        "<div style='padding-top:0.45rem;font-weight:700;font-size:0.88rem;color:#334155;'>⚡ Quick Presets:</div>",
        unsafe_allow_html=True,
    )
with p1:
    st.button(
        "💰 Budget Phone",
        use_container_width=True,
        on_click=apply_preset,
        args=(
            {
                "device_brand": "Xiaomi",
                "os_name": "Android",
                "release_year": 2021,
                "support_5g": "no",
                "screen_size": 16.50,
                "ram": 4.0,
                "internal_memory": 64.0,
                "battery": 5000,
                "rear_camera_mp": 13.0,
                "front_camera_mp": 8.0,
                "launch_price_inr": 12000,
            },
        ),
    )
with p2:
    st.button(
        "🚀 Mid-Range 5G",
        use_container_width=True,
        on_click=apply_preset,
        args=(
            {
                "device_brand": "OnePlus",
                "os_name": "Android",
                "release_year": 2023,
                "support_5g": "yes",
                "screen_size": 17.00,
                "ram": 8.0,
                "internal_memory": 128.0,
                "battery": 5000,
                "rear_camera_mp": 50.0,
                "front_camera_mp": 16.0,
                "launch_price_inr": 32000,
            },
        ),
    )
with p3:
    st.button(
        "👑 Apple Flagship",
        use_container_width=True,
        on_click=apply_preset,
        args=(
            {
                "device_brand": "Apple",
                "os_name": "iOS",
                "release_year": 2023,
                "support_5g": "yes",
                "screen_size": 15.50,
                "ram": 6.0,
                "internal_memory": 256.0,
                "battery": 3349,
                "rear_camera_mp": 48.0,
                "front_camera_mp": 12.0,
                "launch_price_inr": 89900,
            },
        ),
    )
with p4:
    st.button(
        "🔄 Reset Default",
        use_container_width=True,
        on_click=apply_preset,
        args=(DEFAULTS,),
    )

st.write("")

# --------------------------------------------------------------------
# 3-Column Interactive Specification Cards
# --------------------------------------------------------------------
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    with st.container(border=True):
        st.markdown(
            """
<div class="section-header">
<span class="section-icon">🏷️</span>
<h3 class="section-title">Brand & Platform</h3>
</div>
""",
            unsafe_allow_html=True,
        )
        device_brand = st.selectbox("Device Brand", BRANDS, key="device_brand")
        os_name = st.selectbox("Operating System", OS_LIST, key="os_name")
        release_year = st.slider("Release Year", min_value=2012, max_value=2026, step=1, key="release_year")
        support_5g = st.radio(
            "5G Connectivity",
            options=["yes", "no"],
            format_func=lambda x: "5G Enabled" if x == "yes" else "No 5G (4G / Legacy)",
            horizontal=True,
            key="support_5g",
        )

with col2:
    with st.container(border=True):
        st.markdown(
            """
<div class="section-header">
<span class="section-icon">⚙️</span>
<h3 class="section-title">Hardware & Display</h3>
</div>
""",
            unsafe_allow_html=True,
        )
        screen_size = st.number_input(
            "Screen Size (cm)", min_value=5.0, max_value=35.0, step=0.10, format="%.2f", key="screen_size"
        )
        ram = st.select_slider(
            "RAM Capacity (GB)", options=[0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 16.0, 24.0], key="ram"
        )
        internal_memory = st.select_slider(
            "Internal Storage (GB)", options=[8.0, 16.0, 32.0, 64.0, 128.0, 256.0, 512.0, 1024.0], key="internal_memory"
        )
        battery = st.number_input("Battery Capacity (mAh)", min_value=500, max_value=15000, step=100, key="battery")

with col3:
    with st.container(border=True):
        st.markdown(
            """
<div class="section-header">
<span class="section-icon">📸</span>
<h3 class="section-title">Cameras & Launch Price</h3>
</div>
""",
            unsafe_allow_html=True,
        )
        rear_camera_mp = st.number_input(
            "Primary Rear Camera (MP)", min_value=0.0, max_value=250.0, step=1.0, format="%.2f", key="rear_camera_mp"
        )
        front_camera_mp = st.number_input(
            "Front Selfie Camera (MP)", min_value=0.0, max_value=100.0, step=1.0, format="%.2f", key="front_camera_mp"
        )
        launch_price_inr = st.number_input(
            "Original Launch Price (₹ INR)",
            min_value=500,
            max_value=500000,
            step=500,
            help="Original retail launch price in Indian Rupees.",
            key="launch_price_inr",
        )

        launch_price_usd = launch_price_inr / inr_per_usd
        normalized_new_price = float(np.log(launch_price_usd))

        st.markdown(
            f"""
<div class="conversion-pill">
<span>USD: <strong>${launch_price_usd:,.2f}</strong></span>
<span>Log Index: <strong>{normalized_new_price:.3f}</strong></span>
</div>
""",
            unsafe_allow_html=True,
        )

st.write("")
submitted = st.button("✨ Calculate Resale Valuation", type="primary", use_container_width=True)

# --------------------------------------------------------------------
# Valuation Results (Calculated Strictly Upon Button Click)
# --------------------------------------------------------------------
if submitted:
    input_df = pd.DataFrame(
        [
            {
                "device_brand": device_brand,
                "os": os_name,
                "5g": support_5g,
                "screen_size": float(screen_size),
                "rear_camera_mp": float(rear_camera_mp),
                "front_camera_mp": float(front_camera_mp),
                "internal_memory": float(internal_memory),
                "ram": float(ram),
                "battery": float(battery),
                "release_year": int(release_year),
                "normalized_new_price": normalized_new_price,
            }
        ]
    )

    pred_normalized = float(model.predict(input_df)[0])
    pred_usd = float(np.exp(pred_normalized))
    pred_inr = pred_usd * inr_per_usd

    retention_pct = min(max((pred_inr / launch_price_inr) * 100, 0.0), 100.0)
    depreciation_inr = max(launch_price_inr - pred_inr, 0.0)

    st.markdown("### 📊 Valuation Report")
    res_col1, res_col2, res_col3 = st.columns(3, gap="medium")

    with res_col1:
        st.markdown(
            f"""
<div class="metric-card-primary">
<div class="metric-label">Estimated Resale Value (INR)</div>
<div class="metric-value">₹{pred_inr:,.0f}</div>
<div class="metric-sub">Suggested secondary market price</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with res_col2:
        st.markdown(
            f"""
<div class="metric-card-secondary">
<div class="metric-label">USD Equivalent</div>
<div class="metric-value">${pred_usd:,.2f}</div>
<div class="metric-sub">Predicted Log Index: {pred_normalized:.3f}</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with res_col3:
        st.markdown(
            f"""
<div class="metric-card-secondary">
<div class="metric-label">Value Retained</div>
<div class="metric-value">{retention_pct:.1f}%</div>
<div class="metric-sub">Est. Depreciation: ₹{depreciation_inr:,.0f}</div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.write("")
    with st.container(border=True):
        st.markdown(
            f"""
<div style="display:flex;justify-content:space-between;align-items:center;">
<span style="font-weight:700;color:#0f172a;">Resale Value Retention Curve</span>
<span style="font-weight:700;color:#059669;">{retention_pct:.1f}% of ₹{launch_price_inr:,}</span>
</div>
<div class="retention-track">
<div class="retention-fill" style="width:{retention_pct:.1f}%;"></div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.caption(
            f"Evaluated Profile: {device_brand} ({os_name}, {release_year}) • "
            f"{ram:g} GB RAM / {internal_memory:g} GB Storage • {screen_size:.1f} cm Display • "
            f"{battery:,} mAh • {rear_camera_mp:g} MP / {front_camera_mp:g} MP Cameras • "
            f"5G: {support_5g.upper()}"
        )
else:
    st.markdown(
        """
<div class="ready-banner">
Adjust any specifications or select a preset above, then click <b>✨ Calculate Resale Valuation</b> to generate the predicted resale value.
</div>
""",
        unsafe_allow_html=True,
    )
