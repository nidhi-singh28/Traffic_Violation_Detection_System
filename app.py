import streamlit as st
from utils.styles import render_css, divider
from utils.supabase_client import (
    sign_in, sign_out, get_current_session,
    get_user_profile
)

st.set_page_config(
    page_title="Traffic Challan Management",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_css()


def init_session_state():
    defaults = {
        "authenticated": False,
        "user": None,
        "profile": None,
        "current_page": "dashboard",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_session_state()


def check_auth():
    if st.session_state.authenticated and st.session_state.user:
        if not st.session_state.profile:
            profile = get_user_profile(st.session_state.user.id)
            st.session_state.profile = profile
        return True
    return False


def login_page():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
        section[data-testid="stMain"] { margin-left: 0 !important; }
        section[data-testid="stMain"] > div { max-width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;padding:40px 0 20px 0;">
        <div style="font-size:3.5rem;margin-bottom:8px;">🚦</div>
        <h1 style="margin:0;font-size:2.8rem;font-weight:800;line-height:1.25;background:linear-gradient(135deg, #ffb6c1 0%, #3a7bd5 50%, #000000 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
            Traffic Challan<br>Management System
        </h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="text-align:center;color:#8b8fa3;margin:8px 0 30px 0;font-size:0.95rem;">Sign in to manage traffic violations and challans</div>', unsafe_allow_html=True)

    divider()

    st.info("Demo access: **admin@traffic-demo.app / demo123** (Super Admin) or **subadmin@traffic-demo.app / demo123** (Sub Admin).")

    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email", placeholder="admin@traffic-demo.app")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Sign In", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("Please fill in all fields")
            else:
                try:
                    response = sign_in(email, password)
                    if response.user:
                        st.session_state.authenticated = True
                        st.session_state.user = response.user
                        profile = get_user_profile(response.user.id)
                        st.session_state.profile = profile
                        st.rerun()
                except Exception as e:
                    error_msg = str(e)
                    if "Invalid login credentials" in error_msg:
                        st.error("Invalid email or password")
                    else:
                        st.error(f"Login failed: {error_msg}")


def sidebar_navigation():
    profile = st.session_state.profile
    role = profile.get("role", "sub_admin") if profile else "sub_admin"
    name = profile.get("full_name", "User") if profile else "User"
    email = profile.get("email", "") if profile else ""

    with st.sidebar:
        st.markdown(f"""
        <div style="padding:16px 0 8px 0;">
            <div style="font-size:1.15rem;font-weight:700;line-height:1.4;" class="gradient-text">🚦 Traffic Challan<br>Management System</div>
        </div>
        <div class="divider-glow"></div>
        <div style="padding:12px 0;">
            <div style="font-size:0.95rem;font-weight:600;color:#e0e0e0;">{name}</div>
            <div style="font-size:0.75rem;color:#5a5e73;">{email}</div>
            <div style="margin-top:6px;">{f'<span class="badge badge-super">SUPER ADMIN</span>' if role == 'super_admin' else '<span class="badge badge-sub">SUB ADMIN</span>'}</div>
        </div>
        <div class="divider-glow"></div>
        """, unsafe_allow_html=True)

        pages = []
        if role == "super_admin":
            pages = [
                ("dashboard", "📊", "Dashboard"),
                ("challans", "📋", "Challan History"),
                ("violations", "🔍", "Violation Detections"),
                ("rules", "📜", "Traffic Rules"),
                ("subadmins", "👥", "Sub Admins"),
                ("detect", "📷", "Detect Violation"),
            ]
        else:
            pages = [
                ("dashboard", "📊", "My Dashboard"),
                ("challans", "📋", "My Challans"),
                ("detect", "📷", "Detect Violation"),
                ("rules", "📜", "Traffic Rules"),
            ]

        for page_id, icon, label in pages:
            is_active = st.session_state.current_page == page_id
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icon}  {label}", key=f"nav_{page_id}", type=btn_type, use_container_width=True):
                st.session_state.current_page = page_id
                st.rerun()

        st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)

        if st.button("🚪  Sign Out", use_container_width=True):
            sign_out()
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.profile = None
            st.session_state.current_page = "dashboard"
            st.rerun()


def render_page():
    profile = st.session_state.profile
    role = profile.get("role", "sub_admin") if profile else "sub_admin"
    page = st.session_state.current_page

    if page == "dashboard":
        if role == "super_admin":
            from pages.super_admin_dashboard import render
            render()
        else:
            from pages.sub_admin_dashboard import render
            render()
    elif page == "challans":
        if role == "super_admin":
            from pages.challan_history import render
            render()
        else:
            from pages.my_challans import render
            render()
    elif page == "violations":
        from pages.violation_detections import render
        render()
    elif page == "rules":
        if role == "super_admin":
            from pages.traffic_rules import render
            render()
        else:
            from pages.traffic_rules_view import render
            render()
    elif page == "subadmins":
        from pages.sub_admin_management import render
        render()
    elif page == "detect":
        from pages.detect_violation import render
        render()


if not check_auth():
    login_page()
else:
    sidebar_navigation()
    render_page()
