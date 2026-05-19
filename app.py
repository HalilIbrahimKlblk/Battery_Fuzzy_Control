import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────────
# SAYFA YAPILANDIRMASI
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pil Sıcaklık Yönetimi",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# ÖZEL CSS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-primary: #06080f;
        --bg-secondary: #0c1220;
        --bg-card: rgba(15, 23, 42, 0.6);
        --bg-glass: rgba(15, 25, 50, 0.45);
        --border-glass: rgba(99, 102, 241, 0.15);
        --border-hover: rgba(99, 102, 241, 0.35);
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --accent-blue: #3b82f6;
        --accent-cyan: #06b6d4;
        --accent-violet: #8b5cf6;
        --accent-rose: #f43f5e;
        --accent-amber: #f59e0b;
        --accent-emerald: #10b981;
        --glow-blue: 0 0 20px rgba(59,130,246,0.15);
        --glow-violet: 0 0 20px rgba(139,92,246,0.15);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    /* Üst ve alt taraftaki fazla boşlukları sıfırlama */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 0.5rem !important;
    }

    .stApp, [data-testid="stAppViewContainer"] {
        background: var(--bg-primary) !important;
        background-image:
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(59,130,246,0.08), transparent),
            radial-gradient(ellipse 60% 40% at 80% 100%, rgba(139,92,246,0.06), transparent) !important;
    }

    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #080d1a 0%, #0a1128 50%, #0c0f1f 100%) !important;
        border-right: 1px solid rgba(99,102,241,0.1) !important;
    }

    /* Selectbox imleç (cursor) düzeltmesi */
    div[data-testid="stSelectbox"] * {
        cursor: pointer !important;
    }
    div[data-testid="stSelectbox"] input {
        cursor: pointer !important;
        caret-color: transparent; /* Yazı imlecini gizle */
    }

    .hero-container {
        text-align: center;
        padding: 0rem 0 0.5rem 0;
        position: relative;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -40px; left: 50%; transform: translateX(-50%);
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
    }
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -2px;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 40%, #f472b6 70%, #fb923c 100%);
        background-size: 200% 200%;
        animation: gradientShift 6s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        position: relative;
        z-index: 1;
    }
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    .subtitle {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: var(--text-muted);
        letter-spacing: 2.5px;
        text-transform: uppercase;
        position: relative;
        z-index: 1;
    }
    .hero-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99,102,241,0.3), rgba(244,63,94,0.2), transparent);
        margin: 1rem 0;
        border: none;
    }

    .metric-card {
        background: var(--bg-glass);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 1.4rem 1.6rem;
        border-radius: 16px;
        border: 1px solid var(--border-glass);
        margin: 0.4rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-blue), var(--accent-violet));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .metric-card:hover {
        border-color: var(--border-hover);
        box-shadow: var(--glow-violet);
        transform: translateY(-2px);
    }
    .metric-card:hover::before { opacity: 1; }
    .metric-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1.8px;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 2.4rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.1;
    }
    .metric-card-max { border-left: 3px solid var(--accent-rose); }
    .metric-card-max .metric-value { color: #fda4af; }
    .metric-card-mid { border-left: 3px solid var(--accent-cyan); }
    .metric-card-mid .metric-value { color: #67e8f9; }
    .metric-card-pasif { border-left: 3px solid var(--accent-amber); }
    .metric-card-pasif .metric-value { color: #fde68a; }

    .section-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 1.8rem 0 0.8rem 0;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid rgba(99,102,241,0.12);
        letter-spacing: -0.3px;
    }
    .section-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.6rem;
        color: var(--accent-violet);
        text-transform: uppercase;
        letter-spacing: 2px;
        display: block;
        margin-bottom: 0.3rem;
    }

    .rule-box {
        background: var(--bg-glass);
        backdrop-filter: blur(10px);
        border-left: 3px solid var(--accent-blue);
        padding: 0.7rem 1.1rem;
        margin: 0.35rem 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #cbd5e1;
        border-radius: 8px;
        transition: all 0.25s ease;
        border-top: 1px solid rgba(99,102,241,0.06);
        border-right: 1px solid rgba(99,102,241,0.06);
        border-bottom: 1px solid rgba(99,102,241,0.06);
    }
    .rule-box:hover {
        border-left-color: var(--accent-violet);
        background: rgba(15, 25, 50, 0.7);
        transform: translateX(3px);
    }

    .log-entry {
        background: var(--bg-glass);
        backdrop-filter: blur(10px);
        border-left: 3px solid var(--accent-emerald);
        padding: 0.65rem 1.1rem;
        margin: 0.35rem 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        color: #cbd5e1;
        border-radius: 8px;
    }
    .log-entry-max { border-left-color: var(--accent-rose); }
    .log-entry-mid { border-left-color: var(--accent-cyan); }
    .log-entry-pasif { border-left-color: var(--accent-amber); }
    
    .log-badge {
        display: inline-block;
        padding: 0.15rem 0.55rem;
        border-radius: 999px;
        font-size: 0.65rem;
        font-weight: 600;
        margin-right: 0.6rem;
        letter-spacing: 0.5px;
    }
    .badge-max { background: rgba(244,63,94,0.15); color: #fda4af; border: 1px solid rgba(244,63,94,0.25); }
    .badge-mid { background: rgba(6,182,212,0.15); color: #67e8f9; border: 1px solid rgba(6,182,212,0.25); }
    .badge-pasif { background: rgba(245,158,11,0.15); color: #fde68a; border: 1px solid rgba(245,158,11,0.25); }
    
    .footer-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--text-muted);
        text-align: center;
        padding: 0.5rem 0 0rem 0;
        border-top: 1px solid rgba(99,102,241,0.08);
        margin-top: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# CANLI LOG VE BEKLEME MODU BELLEĞİ
# ──────────────────────────────────────────────────────────────────────────────
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'log_counter' not in st.session_state:
    st.session_state.log_counter = 0
if 'app_started' not in st.session_state:
    st.session_state.app_started = False

def reset_simulation():
    """Herhangi bir girdi değiştiğinde uygulamayı tekrar bekleme moduna alır."""
    st.session_state.app_started = False

# ──────────────────────────────────────────────────────────────────────────────
# 1. EVRENLER VE DEĞİŞKENLER
# ──────────────────────────────────────────────────────────────────────────────
sicaklik = ctrl.Antecedent(np.arange(0, 61, 1), 'sicaklik')
yuk = ctrl.Antecedent(np.arange(0, 101, 1), 'yuk')
dis_ortam = ctrl.Antecedent(np.arange(-10, 51, 1), 'dis_ortam')
hiz = ctrl.Antecedent(np.arange(0, 161, 1), 'hiz')
sarj = ctrl.Antecedent(np.arange(0, 101, 1), 'sarj')
klima = ctrl.Antecedent(np.arange(0, 101, 1), 'klima')
pompa = ctrl.Consequent(np.arange(0, 101, 1), 'pompa')

# ──────────────────────────────────────────────────────────────────────────────
# 2. ÜYELİK FONKSİYONLARI
# ──────────────────────────────────────────────────────────────────────────────
sicaklik['dusuk'] = fuzz.trapmf(sicaklik.universe, [0, 0, 15, 20])
sicaklik['optimum'] = fuzz.trimf(sicaklik.universe, [15, 25, 35])
sicaklik['yuksek'] = fuzz.trimf(sicaklik.universe, [30, 40, 50])
sicaklik['kritik'] = fuzz.trapmf(sicaklik.universe, [45, 55, 60, 60])

yuk['sakin'] = fuzz.trapmf(yuk.universe, [0, 0, 20, 35])
yuk['normal'] = fuzz.trimf(yuk.universe, [25, 45, 70])
yuk['agresif'] = fuzz.trapmf(yuk.universe, [60, 80, 100, 100])

dis_ortam['soguk'] = fuzz.trapmf(dis_ortam.universe, [-10, -10, 5, 15])
dis_ortam['ilik'] = fuzz.trimf(dis_ortam.universe, [10, 20, 30])
dis_ortam['sicak'] = fuzz.trapmf(dis_ortam.universe, [25, 35, 50, 50])

hiz['yavas'] = fuzz.trapmf(hiz.universe, [0, 0, 30, 50])
hiz['orta'] = fuzz.trimf(hiz.universe, [40, 70, 100])
hiz['yuksek'] = fuzz.trapmf(hiz.universe, [90, 120, 160, 160])

sarj['dusuk'] = fuzz.trapmf(sarj.universe, [0, 0, 10, 20])
sarj['orta'] = fuzz.trimf(sarj.universe, [15, 50, 85])
sarj['tam_dolu'] = fuzz.trapmf(sarj.universe, [80, 90, 100, 100])

klima['kapali'] = fuzz.trapmf(klima.universe, [0, 0, 5, 15])
klima['dusuk'] = fuzz.trimf(klima.universe, [10, 25, 50])
klima['yuksek'] = fuzz.trapmf(klima.universe, [40, 70, 100, 100])

pompa['pasif'] = fuzz.trapmf(pompa.universe, [0, 0, 10, 20])
pompa['dusuk'] = fuzz.trimf(pompa.universe, [15, 30, 45])
pompa['orta'] = fuzz.trimf(pompa.universe, [35, 50, 65])
pompa['yuksek'] = fuzz.trimf(pompa.universe, [60, 72, 85])
pompa['maksimum'] = fuzz.trapmf(pompa.universe, [80, 90, 100, 100])

# ──────────────────────────────────────────────────────────────────────────────
# 3. KURAL TABANI (20 Adet)
# ──────────────────────────────────────────────────────────────────────────────
RULES_TEXT = []
def add_r(rule, text):
    RULES_TEXT.append(text)
    return rule

kurallar = [
    add_r(ctrl.Rule(sicaklik['dusuk'], pompa['pasif']), "R01: Sıcaklık DÜŞÜK → Pompa Gücü PASİF"),
    add_r(ctrl.Rule(sicaklik['optimum'], pompa['dusuk']), "R02: Sıcaklık OPTİMUM → Pompa Gücü DÜŞÜK"),
    add_r(ctrl.Rule(sicaklik['yuksek'], pompa['orta']), "R03: Sıcaklık YÜKSEK → Pompa Gücü ORTA"),
    add_r(ctrl.Rule(sicaklik['kritik'], pompa['maksimum']), "R04: Sıcaklık KRİTİK → Pompa Gücü MAKSİMUM"),
    add_r(ctrl.Rule(yuk['agresif'] & dis_ortam['sicak'], pompa['yuksek']), "R05: Motor Yükü AGRESİF ∧ Dış Ortam SICAK → Pompa Gücü YÜKSEK"),
    add_r(ctrl.Rule(sicaklik['optimum'] & yuk['sakin'] & dis_ortam['ilik'], pompa['dusuk']), "R06: Sıcaklık OPTİMUM ∧ Sürüş SAKİN ∧ Dış Ortam ILIK → Pompa Gücü DÜŞÜK"),
    add_r(ctrl.Rule(sicaklik['yuksek'] & hiz['yavas'] & klima['yuksek'], pompa['yuksek']), "R07: Sıcaklık YÜKSEK ∧ Hız YAVAŞ ∧ Klima YÜKSEK → Pompa Gücü YÜKSEK"),
    add_r(ctrl.Rule(sicaklik['yuksek'] & hiz['yuksek'] & dis_ortam['soguk'], pompa['orta']), "R08: Sıcaklık YÜKSEK ∧ Hız YÜKSEK ∧ Dış Ortam SOĞUK → Pompa Gücü ORTA"),
    add_r(ctrl.Rule(sicaklik['kritik'] & sarj['tam_dolu'] & yuk['agresif'], pompa['maksimum']), "R09: Sıcaklık KRİTİK ∧ Şarj TAM DOLU ∧ Yük AGRESİF → Pompa Gücü MAKSİMUM"),
    add_r(ctrl.Rule(sicaklik['optimum'] & klima['kapali'] & dis_ortam['soguk'], pompa['pasif']), "R10: Sıcaklık OPTİMUM ∧ Klima KAPALI ∧ Dış Ortam SOĞUK → Pompa Gücü PASİF"),
    add_r(ctrl.Rule(sicaklik['yuksek'] & yuk['normal'] & sarj['orta'], pompa['orta']), "R11: Sıcaklık YÜKSEK ∧ Yük NORMAL ∧ Şarj ORTA → Pompa Gücü ORTA"),
    add_r(ctrl.Rule(yuk['agresif'] & hiz['yavas'] & dis_ortam['sicak'], pompa['maksimum']), "R12: Yük AGRESİF ∧ Hız YAVAŞ ∧ Dış Ortam SICAK → Pompa Gücü MAKSİMUM"),
    add_r(ctrl.Rule(sicaklik['dusuk'] & dis_ortam['soguk'] & klima['yuksek'], pompa['pasif']), "R13: Sıcaklık DÜŞÜK ∧ Dış Ortam SOĞUK ∧ Klima YÜKSEK → Pompa Gücü PASİF"),
    add_r(ctrl.Rule(sarj['dusuk'] & yuk['sakin'] & sicaklik['optimum'], pompa['dusuk']), "R14: Şarj DÜŞÜK ∧ Sürüş SAKİN ∧ Sıcaklık OPTİMUM → Pompa Gücü DÜŞÜK"),
    add_r(ctrl.Rule(sicaklik['yuksek'] & klima['yuksek'] & dis_ortam['sicak'], pompa['maksimum']), "R15: Sıcaklık YÜKSEK ∧ Klima YÜKSEK ∧ Dış Ortam SICAK → Pompa Gücü MAKSİMUM"),
    add_r(ctrl.Rule(hiz['yuksek'] & yuk['normal'] & dis_ortam['ilik'], pompa['orta']), "R16: Hız YÜKSEK ∧ Yük NORMAL ∧ Dış Ortam ILIK → Pompa Gücü ORTA"),
    add_r(ctrl.Rule(sicaklik['kritik'] & hiz['yavas'] & klima['kapali'], pompa['maksimum']), "R17: Sıcaklık KRİTİK ∧ Hız YAVAŞ ∧ Klima KAPALI → Pompa Gücü MAKSİMUM"),
    add_r(ctrl.Rule(sicaklik['optimum'] & yuk['agresif'] & sarj['tam_dolu'], pompa['orta']), "R18: Sıcaklık OPTİMUM ∧ Yük AGRESİF ∧ Şarj TAM DOLU → Pompa Gücü ORTA"),
    add_r(ctrl.Rule(dis_ortam['sicak'] & klima['dusuk'] & hiz['orta'], pompa['orta']), "R19: Dış Ortam SICAK ∧ Klima DÜŞÜK ∧ Hız ORTA → Pompa Gücü ORTA"),
    add_r(ctrl.Rule(sicaklik['dusuk'] & yuk['normal'] & sarj['orta'], pompa['pasif']), "R20: Sıcaklık DÜŞÜK ∧ Yük NORMAL ∧ Şarj ORTA → Pompa Gücü PASİF")
]

kontrol_sistemi = ctrl.ControlSystem(kurallar)
ev_sim = ctrl.ControlSystemSimulation(kontrol_sistemi)

# ──────────────────────────────────────────────────────────────────────────────
# GRAFİK FONKSİYONLARI
# ──────────────────────────────────────────────────────────────────────────────
def draw_input(variable, cur_val, title):
    fig, ax = plt.subplots(figsize=(8, 3.2), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    colors = ['#0ea5e9', '#22d3ee', '#10b981', '#f59e0b', '#ef4444']
    for i, term in enumerate(variable.terms):
        mf = variable[term].mf
        c = colors[i % len(colors)]
        ax.plot(variable.universe, mf, linewidth=2, color=c, label=term)
        ax.fill_between(variable.universe, 0, mf, alpha=0.1, color=c)
    ax.axvline(cur_val, color='#fbbf24', linestyle='--', linewidth=1.5)
    ax.set_title(title, color='#f1f5f9', fontsize=11, fontweight='bold')
    ax.tick_params(colors='#94a3b8')
    ax.grid(True, alpha=0.1, color='#475569')
    ax.legend(loc='upper right', facecolor='#1e293b', labelcolor='#e2e8f0', fontsize=8)
    plt.tight_layout()
    return fig

# ──────────────────────────────────────────────────────────────────────────────
# BAŞLIK ALANI
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="main-title">🔋 Batarya Sıcaklık Yönetim Paneli</div>
    <div class="subtitle">Bulanık Mantık Tabanlı Batarya Soğutma Sistemi Kontrolcüsü</div>
</div>
<div class="hero-divider"></div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# ÇEŞİTLENDİRİLMİŞ GİRİŞ ENSTRÜMANLARI
# ──────────────────────────────────────────────────────────────────────────────
st.sidebar.markdown("<h1 style='text-align:center; color:white;'>⚙️ Giriş Değerleri</h1>", unsafe_allow_html=True)
st.sidebar.divider()

val_sicaklik = st.sidebar.slider("🌡️ Batarya Sıcaklığı (°C)", 0, 60, 25, on_change=reset_simulation)
val_yuk = st.sidebar.slider("⚡ Motor Akım Yükü (%)", 0, 100, 40, on_change=reset_simulation)
val_dis_ortam = st.sidebar.slider("🌍 Dış Ortam Sıcaklığı (°C)", -10, 50, 22, on_change=reset_simulation)

val_hiz = st.sidebar.number_input("🚗 Araç Hızı (km/h)", min_value=0, max_value=220, value=50, step=5, on_change=reset_simulation)
val_sarj = st.sidebar.number_input("🔋 Şarj Seviyesi SoC (%)", min_value=0, max_value=100, value=80, on_change=reset_simulation)

val_klima = st.sidebar.selectbox("❄️ Kabin Klima Talebi (%)", list(range(0, 101, 10)), index=2, on_change=reset_simulation)

st.sidebar.divider()
hesapla = st.sidebar.button("🚀 UYGULAMAYI BAŞLAT", use_container_width=True, type="primary")

if hesapla:
    st.session_state.app_started = True

# ──────────────────────────────────────────────────────────────────────────────
# SİSTEM BEKLEME MODU KONTROLÜ
# ──────────────────────────────────────────────────────────────────────────────
if not st.session_state.app_started:
    # Bekleme Ekranı
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; background: var(--bg-glass); backdrop-filter: blur(10px); border: 1px dashed var(--border-glass); border-radius: 16px; margin: 2rem 0;">
        <h2 style="color: var(--accent-blue); margin-bottom: 1rem; font-weight: 700;">⏳ Sistem Bekleme Modunda</h2>
        <p style="color: var(--text-muted); font-size: 1.1rem;">Uygulamayı başlatmak için sol menüden parametreleri ayarlayın ve 'Uygulamayı Başlat' butonuna tıklayın.</p>
    </div>
    """, unsafe_allow_html=True)

else:
    # ──────────────────────────────────────────────────────────────────────────────
    # SİMÜLASYON VE VERİ GÜNCELLEME
    # ──────────────────────────────────────────────────────────────────────────────
    ev_sim.input['sicaklik'] = val_sicaklik
    ev_sim.input['yuk'] = val_yuk
    ev_sim.input['dis_ortam'] = val_dis_ortam
    ev_sim.input['hiz'] = val_hiz
    ev_sim.input['sarj'] = val_sarj
    ev_sim.input['klima'] = val_klima

    ev_sim.compute()
    hesaplanan_pompa = ev_sim.output['pompa']

    # Log ekleme işlemi sadece butona basıldığında gerçekleşir
    if hesapla:
        st.session_state.log_counter += 1
        m_text = "MAKSİMUM GÜÇ" if hesaplanan_pompa > 75 else ("DENGELİ MOD" if hesaplanan_pompa > 35 else "TERMAL PASİF")
        st.session_state.logs.append({
            'No': st.session_state.log_counter,
            'Zaman': datetime.now().strftime('%H:%M:%S'),
            'Batarya Sıcaklık': val_sicaklik,
            'Motor Akımı': val_yuk,
            'Dış Ortam': val_dis_ortam,
            'Hız': val_hiz,
            'SoC': val_sarj,
            'Klima Yükü': val_klima,
            'Pompa Gücü': round(hesaplanan_pompa, 2),
            'Mod': m_text
        })

    # Sonuç Panelleri
    mode_css = "metric-card-max" if hesaplanan_pompa > 75 else ("metric-card-mid" if hesaplanan_pompa > 35 else "metric-card-pasif")
    mode_emoji = "🚨" if hesaplanan_pompa > 75 else ("⚡" if hesaplanan_pompa > 35 else "⏸️")
    mode_name = "TERMAL REAKSİYON" if hesaplanan_pompa > 75 else ("STABİL SOĞUTMA" if hesaplanan_pompa > 35 else "GÜÇ TASARRUFU")

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"""
        <div class="metric-card {mode_css}">
            <div class="metric-label">{mode_emoji} Isıl Yönetim Statüsü</div>
            <div class="metric-value" style="font-size:1.6rem;">{mode_name}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">❄️ Kompresör Sinyal Genliği (PWM)</div>
            <div class="metric-value">% {hesaplanan_pompa:.2f}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🪛 Mod Türü</div>
            <div class="metric-value" style="font-size: 1.6rem;">{m_text}</div>
        </div>""", unsafe_allow_html=True)
        
    with c2:
        st.subheader("📈 Çıkış (Durulaştırma) Grafiği")
        pompa.view(sim=ev_sim)
        fig_out = plt.gcf()
        fig_out.set_size_inches(8, 3.5)
        fig_out.patch.set_facecolor('#06080f')
        st.pyplot(fig_out)
        plt.close(fig_out)

    st.divider()

    # Grafik Bölümü
    st.markdown('<div class="section-header"><span class="section-tag">Membership Functions</span>📐 Ana Sensör Katmanları Üyelik Analizi</div>', unsafe_allow_html=True)
    g_col1, g_col2, g_col3 = st.columns(3)
    with g_col1:
        st.pyplot(draw_input(sicaklik, val_sicaklik, "Batarya İç Sıcaklığı Üyelik Fonksiyonu"))
    with g_col2:
        st.pyplot(draw_input(yuk, val_yuk, "Anlık Motor Akım Talebi Üyelik Fonksiyonu"))
    with g_col3:
        st.pyplot(draw_input(dis_ortam, val_dis_ortam, "Dış Ortam Termal Spektrumu"))

    # ──────────────────────────────────────────────────────────────────────────────
    # SİSTEM LOGLAR
    # ──────────────────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header"><span class="section-tag">System Log</span>📋 Batarya Sıcaklık Log Verileri</div>', unsafe_allow_html=True)
    if st.session_state.logs:
        recent_logs = list(reversed(st.session_state.logs[-3:]))
        for entry in recent_logs:
            c_style = "log-entry log-entry-max" if entry['Pompa Gücü'] > 75 else ("log-entry log-entry-mid" if entry['Pompa Gücü'] > 35 else "log-entry log-entry-pasif")
            b_style = "badge-max" if entry['Pompa Gücü'] > 75 else ("badge-mid" if entry['Pompa Gücü'] > 35 else "badge-pasif")
            st.markdown(f"""
            <div class="{c_style}">
                <span class="log-badge {b_style}">#{entry['No']:03d}</span>
                <strong>[{entry['Zaman']}]</strong> Batarya: {entry['Batarya Sıcaklık']}°C, Akım: %{entry['Motor Akımı']}, Dış: {entry['Dış Ortam']}°C, Hız: {entry['Hız']}km/h | 
                <strong>Pompa Çıktısı: % {entry['Pompa Gücü']}</strong> [{entry['Mod']}]
            </div>""", unsafe_allow_html=True)
            
        with st.expander("📊 Tüm Sürüş / Şarj Termal Matrisini İncele"):
            df_logs = pd.DataFrame(st.session_state.logs)
            st.dataframe(df_logs, use_container_width=True, hide_index=True)
            
            csv_text = df_logs.to_csv(index=False, sep=';')
            csv_bytes = csv_text.encode('utf-8-sig')
            
            st.download_button(
                label="📥 Telemetri Loglarını CSV Olarak İndir", 
                data=csv_bytes, 
                file_name="ev_thermal_ecu_logs.csv", 
                mime="text/csv"
            )

    # ──────────────────────────────────────────────────────────────────────────────
    # AKADEMİK TEST SENARYOLARI
    # ──────────────────────────────────────────────────────────────────────────────
    with st.expander("🧪 Hazır Test Senaryoları"):
        senaryolar = [
            ("S1: Şehir İçi Ekonomik Sürüş", 25, 40, 22, 50, 80, 20),
            ("S2: Otoyol Yüksek Hız Rejimi", 38, 70, 28, 130, 45, 10),
            ("S3: Aşırı Sıcak Hızlı Şarj", 48, 85, 40, 0, 95, 0),
            ("S4: Kış Mevsimi Rejeneratif Koruma", 12, 20, -5, 60, 30, 60)
        ]
        s_rows = []
        for name, s_v, y_v, d_v, h_v, sr_v, k_v in senaryolar:
            try:
                ev_sim.input['sicaklik'] = s_v
                ev_sim.input['yuk'] = y_v
                ev_sim.input['dis_ortam'] = d_v
                ev_sim.input['hiz'] = h_v
                ev_sim.input['sarj'] = sr_v
                ev_sim.input['klima'] = k_v
                ev_sim.compute()
                out_p = ev_sim.output['pompa']
                m_str = "Reaksiyon/Maksimum" if out_p > 75 else ("Dengeli Soğutma" if out_p > 35 else "Güç Tasarrufu")
                s_rows.append([name, s_v, f"%{y_v}", f"{d_v}°C", h_v, f"%{sr_v}", f"%{out_p:.2f}", m_str])
            except:
                s_rows.append([name, s_v, y_v, d_v, h_v, sr_v, "Hata", "Limit Dışı"])
        df_s = pd.DataFrame(s_rows, columns=["Validasyon Senaryosu", "Batarya Sıc.", "Motor Akımı", "Dış Ortam", "Hız (km/h)", "SoC (%)", "Kompresör PWM", "Sistem Modu"])
        st.dataframe(df_s, use_container_width=True, hide_index=True)

# ──────────────────────────────────────────────────────────────────────────────
# SİSTEM BİLGİLERİ VE DOKÜMANTASYON
# ──────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header"><span class="section-tag">System Info</span>ℹ️ Proje Bilgileri</div>', unsafe_allow_html=True)
st.markdown("""
- **Proje Kapsamı**: Bu proje, elektrikli araçlarda batarya sıcaklık yönetimi için bulanık mantık tabanlı bir kontrol sistemi geliştirmeyi amaçlamaktadır. Batarya sıcaklığı, motor akım yükü, dış ortam sıcaklığı, araç hızı, şarj seviyesi ve klima talebi gibi çoklu girdileri değerlendirerek soğutucu gücünü optimize eder.
- **Kullanılan Teknolojiler**: Python programlama dili, Streamlit web frameworkü, scikit-fuzzy kütüphanesi, Matplotlib görselleştirme kütüphanesi.
- **Sistem Bileşenleri**: 
    1. Girdi Değişkenleri: Batarya Sıcaklığı, Motor Akım Yükü, Dış Ortam Sıcaklığı, Araç Hızı, Şarj Seviyesi, Klima Talebi
    2. Çıktı Değişkeni: Kompresör Pompa Gücü (PWM Sinyal Genliği).
    3. Kural Tabanı: 20 adet bulanık kural, farklı sürüş ve çevresel koşullara göre pompa gücünü belirler.
- **Loglama ve Telemetri**: Her hesaplama sonrası sistem, girdi değerleri, hesaplanan pompa gücü, aktif kural modu ve zaman damgası gibi bilgileri içeren bir log kaydı oluşturur. Bu loglar, sürüş boyunca oluşan termal durumları analiz etmek ve sistem performansını değerlendirmek için kullanılabilir.
""", unsafe_allow_html=True)

st.write("")

c1, c2, c3, c4 = st.columns(4)

def create_stat_card(icon, title, value, color):
    return f"""
    <div style="
        background: rgba(15, 25, 50, 0.45); 
        backdrop-filter: blur(10px); 
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(99, 102, 241, 0.15); 
        border-left: 4px solid {color};
        padding: 1.2rem 1rem; 
        border-radius: 12px; 
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    ">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.6rem;">
            {icon} {title}
        </div>
        <div style="font-size: 2rem; font-weight: 800; color: #f1f5f9; line-height: 1;">
            {value}
        </div>
    </div>
    """

with c1:
    st.markdown(create_stat_card("📥", "Girdi Sayısı", "6", "#3b82f6"), unsafe_allow_html=True)
with c2:
    st.markdown(create_stat_card("📤", "Çıktı Sayısı", "1", "#10b981"), unsafe_allow_html=True)
with c3:
    st.markdown(create_stat_card("📜", "Kural Sayısı", "20", "#8b5cf6"), unsafe_allow_html=True)
with c4:
    st.markdown(create_stat_card("🧠", "Çıkarım Modeli", "Mamdani", "#f59e0b"), unsafe_allow_html=True)

st.markdown('<div class="section-header"><span class="section-tag">Documentation</span>🧾 Sistem Dokümantasyonu</div>', unsafe_allow_html=True)
with st.expander("📜 Kural Tabanında Tanımlı Kurallar"):
    for text in RULES_TEXT:
        st.markdown(f"<div class='rule-box'>{text}</div>", unsafe_allow_html=True)

st.markdown("""
<div class="footer-text">
    📚 Bulanık Mantık Dersi Dönem Projesi<br>
    Elektrikli Araçlar İçin Akıllı Batarya Sıcaklık Yönetim Sistemi · 2026
</div>
""", unsafe_allow_html=True)