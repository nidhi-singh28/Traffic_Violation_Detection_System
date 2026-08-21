import streamlit as st

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f1117 0%, #1a1d2e 50%, #0f1117 100%);
    }

    .gradient-text {
        background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 50%, #00d2ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    }

    .gradient-text-warm {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    }

    .gradient-text-green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }

    .gradient-text-gold {
        background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }

    .stat-card {
        background: linear-gradient(145deg, rgba(26, 29, 46, 0.9) 0%, rgba(15, 17, 23, 0.95) 100%);
        border: 1px solid rgba(58, 123, 213, 0.15);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }

    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00d2ff, #3a7bd5, #00d2ff);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .stat-card:hover {
        transform: translateY(-4px);
        border-color: rgba(58, 123, 213, 0.4);
        box-shadow: 0 8px 32px rgba(58, 123, 213, 0.2);
    }

    .stat-card:hover::before {
        opacity: 1;
    }

    .stat-card-warm::before {
        background: linear-gradient(90deg, #f093fb, #f5576c, #f093fb);
    }

    .stat-card-green::before {
        background: linear-gradient(90deg, #11998e, #38ef7d, #11998e);
    }

    .stat-card-gold::before {
        background: linear-gradient(90deg, #f7971e, #ffd200, #f7971e);
    }

    .dashboard-stat-static-anchor + div[data-testid="stButton"] > button {
        pointer-events: none !important;
        cursor: default !important;
    }

    .dashboard-stat-static-anchor + div[data-testid="stButton"] > button:hover,
    .dashboard-stat-static-anchor + div[data-testid="stButton"] > button:focus {
        transform: none !important;
        box-shadow: none !important;
        outline: none !important;
    }

    .stat-card-clickable {
        cursor: pointer;
        pointer-events: none;
    }

    div[data-testid="column"]:has(.stat-card-clickable) div[data-testid="stVerticalBlock"]:has(.stat-card-clickable),
    div[data-testid="stColumn"]:has(.stat-card-clickable) div[data-testid="stVerticalBlock"]:has(.stat-card-clickable) {
        position: relative !important;
    }

    div[data-testid="stElementContainer"]:has(.stat-card-clickable) + div[data-testid="stElementContainer"]:has(div[data-testid="stButton"]) {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        z-index: 10 !important;
        margin: 0 !important;
        height: auto !important;
        min-height: 0 !important;
        overflow: visible !important;
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
    }

    div[data-testid="stElementContainer"]:has(.stat-card-clickable) + div[data-testid="stElementContainer"]:has(div[data-testid="stButton"]) div[data-testid="stButton"] {
        height: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stElementContainer"]:has(.stat-card-clickable) + div[data-testid="stElementContainer"]:has(div[data-testid="stButton"]) button {
        width: 100% !important;
        height: 100% !important;
        min-height: 0 !important;
        opacity: 0 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
        cursor: pointer !important;
        color: transparent !important;
        font-size: 0 !important;
        line-height: 0 !important;
    }

    div[data-testid="stElementContainer"]:has(.stat-card-clickable) + div[data-testid="stElementContainer"]:has(div[data-testid="stButton"]) button:hover,
    div[data-testid="stElementContainer"]:has(.stat-card-clickable) + div[data-testid="stElementContainer"]:has(div[data-testid="stButton"]) button:focus {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        transform: none !important;
    }

    div[data-testid="column"]:has(.stat-card-clickable):has(div[data-testid="stButton"] > button:hover) .stat-card-clickable,
    div[data-testid="stColumn"]:has(.stat-card-clickable):has(div[data-testid="stButton"] > button:hover) .stat-card-clickable,
    div[data-testid="stElementContainer"]:has(.stat-card-clickable):has(+ div[data-testid="stElementContainer"] button:hover) .stat-card-clickable,
    div[data-testid="stElementContainer"]:has(.stat-card-clickable):hover .stat-card-clickable {
        transform: translateY(-4px);
        border-color: rgba(58, 123, 213, 0.4);
        box-shadow: 0 8px 32px rgba(58, 123, 213, 0.2);
    }

    div[data-testid="column"]:has(.stat-card-clickable):has(div[data-testid="stButton"] > button:hover) .stat-card-clickable::before,
    div[data-testid="stColumn"]:has(.stat-card-clickable):has(div[data-testid="stButton"] > button:hover) .stat-card-clickable::before,
    div[data-testid="stElementContainer"]:has(.stat-card-clickable):has(+ div[data-testid="stElementContainer"] button:hover) .stat-card-clickable::before,
    div[data-testid="stElementContainer"]:has(.stat-card-clickable):hover .stat-card-clickable::before {
        opacity: 1;
    }

    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        line-height: 1.2;
        margin: 8px 0;
    }

    .stat-label {
        font-size: 0.85rem;
        color: #8b8fa3;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 500;
    }

    .data-card {
        background: linear-gradient(145deg, rgba(26, 29, 46, 0.8) 0%, rgba(15, 17, 23, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 20px;
        margin: 8px 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
    }

    .data-card:hover {
        border-color: rgba(58, 123, 213, 0.3);
        box-shadow: 0 4px 20px rgba(58, 123, 213, 0.15);
        transform: translateX(4px);
    }

    .rule-card {
        background: linear-gradient(145deg, rgba(26, 29, 46, 0.85) 0%, rgba(15, 17, 23, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 20px 24px;
        margin: 10px 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    }

    .rule-card::after {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: linear-gradient(180deg, #00d2ff, #3a7bd5);
        border-radius: 4px 0 0 4px;
    }

    .rule-card:hover {
        border-color: rgba(58, 123, 213, 0.3);
        box-shadow: 0 6px 24px rgba(58, 123, 213, 0.15);
        transform: translateY(-2px);
    }

    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .badge-pending {
        background: rgba(255, 193, 7, 0.15);
        color: #ffc107;
        border: 1px solid rgba(255, 193, 7, 0.3);
    }

    .badge-approved {
        background: rgba(40, 167, 69, 0.15);
        color: #28a745;
        border: 1px solid rgba(40, 167, 69, 0.3);
    }

    .badge-paid {
        background: rgba(0, 210, 255, 0.15);
        color: #00d2ff;
        border: 1px solid rgba(0, 210, 255, 0.3);
    }

    .badge-disputed {
        background: rgba(245, 87, 108, 0.15);
        color: #f5576c;
        border: 1px solid rgba(245, 87, 108, 0.3);
    }

    .badge-super {
        background: linear-gradient(135deg, rgba(0, 210, 255, 0.2), rgba(58, 123, 213, 0.2));
        color: #00d2ff;
        border: 1px solid rgba(0, 210, 255, 0.3);
    }

    .badge-sub {
        background: rgba(17, 153, 142, 0.15);
        color: #38ef7d;
        border: 1px solid rgba(56, 239, 125, 0.3);
    }

    .badge-active {
        background: rgba(40, 167, 69, 0.15);
        color: #38ef7d;
        border: 1px solid rgba(40, 167, 69, 0.3);
    }

    .badge-inactive {
        background: rgba(245, 87, 108, 0.15);
        color: #f5576c;
        border: 1px solid rgba(245, 87, 108, 0.3);
    }

    .upload-zone {
        background: linear-gradient(145deg, rgba(26, 29, 46, 0.6) 0%, rgba(15, 17, 23, 0.8) 100%);
        border: 2px dashed rgba(58, 123, 213, 0.3);
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        transition: all 0.3s ease;
    }

    .upload-zone:hover {
        border-color: rgba(0, 210, 255, 0.6);
        background: linear-gradient(145deg, rgba(26, 29, 46, 0.8) 0%, rgba(15, 17, 23, 0.9) 100%);
    }

    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid rgba(58, 123, 213, 0.2);
    }

    .login-container {
        max-width: 440px;
        margin: 0 auto;
        padding: 40px;
        background: linear-gradient(145deg, rgba(26, 29, 46, 0.95) 0%, rgba(15, 17, 23, 0.98) 100%);
        border: 1px solid rgba(58, 123, 213, 0.15);
        border-radius: 20px;
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.4);
    }

    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #0f1117 0%, #1a1d2e 100%);
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1117 0%, #1a1d2e 100%);
        border-right: 1px solid rgba(58, 123, 213, 0.1);
    }

    div[data-testid="stSidebarNav"] {
        padding-top: 20px;
    }

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        text-align: left;
        padding: 10px 16px;
        border-radius: 10px;
        transition: all 0.2s ease;
    }

    .stButton > button {
        border-radius: 10px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(58, 123, 213, 0.3);
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        background: rgba(26, 29, 46, 0.8) !important;
        border: 1px solid rgba(58, 123, 213, 0.2) !important;
        border-radius: 10px !important;
        color: #e0e0e0 !important;
        transition: all 0.2s ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        border-color: rgba(0, 210, 255, 0.5) !important;
        box-shadow: 0 0 0 2px rgba(0, 210, 255, 0.1) !important;
    }

    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    .stDataFrame table {
        background: rgba(26, 29, 46, 0.6);
    }

    .stDataFrame thead th {
        background: rgba(26, 29, 46, 0.9) !important;
        color: #00d2ff !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.8rem;
    }

    .stDataFrame tbody td {
        color: #e0e0e0 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }

    .stDataFrame tbody tr:hover {
        background: rgba(58, 123, 213, 0.08) !important;
    }

    .stAlert {
        border-radius: 12px;
        border: 1px solid;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 210, 255, 0.1), rgba(58, 123, 213, 0.1));
        border-bottom: 2px solid #00d2ff;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }

    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    .animate-fade-in {
        animation: fadeInUp 0.5s ease-out forwards;
    }

    .animate-slide-in {
        animation: slideInLeft 0.4s ease-out forwards;
    }

    .animate-pulse {
        animation: pulse 2s ease-in-out infinite;
    }

    .shimmer-text {
        background: linear-gradient(90deg, #00d2ff, #3a7bd5, #00d2ff, #3a7bd5);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s linear infinite;
    }

    .divider-glow {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 210, 255, 0.3), transparent);
        margin: 20px 0;
    }

    .icon-stat {
        font-size: 2rem;
        margin-bottom: 8px;
    }

    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: #5a5e73;
    }

    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 16px;
        opacity: 0.4;
    }

    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .progress-bar-custom {
        height: 6px;
        border-radius: 3px;
        background: rgba(26, 29, 46, 0.8);
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        border-radius: 3px;
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        transition: width 0.5s ease;
    }

    .category-tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        background: rgba(58, 123, 213, 0.15);
        color: #3a7bd5;
        border: 1px solid rgba(58, 123, 213, 0.2);
    }

    .amount-display {
        font-size: 1.3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #f7971e, #ffd200);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .vehicle-number {
        font-family: 'Courier New', monospace;
        font-weight: 700;
        font-size: 1.1rem;
        color: #00d2ff;
        letter-spacing: 1px;
    }

    .stExpander {
        border: 1px solid rgba(58, 123, 213, 0.1);
        border-radius: 12px;
        overflow: hidden;
    }

    .stExpander:hover {
        border-color: rgba(58, 123, 213, 0.25);
    }

    .stMetric {
        background: linear-gradient(145deg, rgba(26, 29, 46, 0.6), rgba(15, 17, 23, 0.8));
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(255, 255, 255, 0.04);
    }

    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 800;
    }

    .stChatInput > div > div > div {
        border-radius: 12px;
        border: 1px solid rgba(58, 123, 213, 0.2);
    }

    .stFileUploader > section {
        border: 2px dashed rgba(58, 123, 213, 0.25);
        border-radius: 14px;
        background: rgba(26, 29, 46, 0.4);
    }

    .stFileUploader > section:hover {
        border-color: rgba(0, 210, 255, 0.5);
    }
</style>
"""


def render_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def gradient_text(text, size="2rem", weight="800"):
    return f'<span style="font-size:{size};font-weight:{weight};background:linear-gradient(135deg,#00d2ff 0%,#3a7bd5 50%,#00d2ff 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{text}</span>'


def gradient_text_warm(text, size="2rem", weight="800"):
    return f'<span style="font-size:{size};font-weight:{weight};background:linear-gradient(135deg,#f093fb 0%,#f5576c 50%,#f093fb 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{text}</span>'


def gradient_text_green(text, size="1.5rem", weight="700"):
    return f'<span style="font-size:{size};font-weight:{weight};background:linear-gradient(135deg,#11998e 0%,#38ef7d 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{text}</span>'


def gradient_text_gold(text, size="1.5rem", weight="700"):
    return f'<span style="font-size:{size};font-weight:{weight};background:linear-gradient(135deg,#f7971e 0%,#ffd200 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{text}</span>'


def stat_card(value, label, card_class="", value_class="gradient-text", clickable=False):
    click_class = " stat-card-clickable" if clickable else ""
    return f"""
    <div class="stat-card {card_class}{click_class} animate-fade-in">
        <div class="stat-number {value_class}">{value}</div>
        <div class="stat-label">{label}</div>
    </div>
    """


def badge(text, badge_type="pending"):
    return f'<span class="badge badge-{badge_type}">{text.upper()}</span>'


def divider():
    st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)


def section_header(text):
    st.markdown(f'<div class="section-header gradient-text" style="font-size:1.5rem;">{text}</div>', unsafe_allow_html=True)


def empty_state(icon, message):
    st.markdown(f"""
    <div class="empty-state animate-fade-in">
        <div class="empty-state-icon">{icon}</div>
        <div style="font-size:1.1rem;margin-bottom:8px;">{message}</div>
    </div>
    """, unsafe_allow_html=True)
