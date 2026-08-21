import streamlit as st
from utils.styles import gradient_text, gradient_text_warm, badge, divider, empty_state, stat_card
from utils.supabase_client import (
    get_all_profiles, create_sub_admin, toggle_sub_admin_active, delete_sub_admin
)


def render():
    st.markdown(f"""
    <div class="animate-fade-in" style="margin-bottom:24px;">
        <h1 style="margin:0;font-size:2rem;">{gradient_text("Sub Admin Management")}</h1>
        <p style="color:#5a5e73;margin:4px 0 0 0;font-size:0.9rem;">Add, manage, and remove sub administrators</p>
    </div>
    """, unsafe_allow_html=True)

    profiles = get_all_profiles()
    subadmins = [p for p in profiles if p.get("role") == "sub_admin"]
    active_count = len([s for s in subadmins if s.get("is_active", True)])
    inactive_count = len(subadmins) - active_count

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(stat_card(len(subadmins), "Total Sub Admins", "", "gradient-text"), unsafe_allow_html=True)
    with col2:
        st.markdown(stat_card(active_count, "Active", "stat-card-green", "gradient-text-warm"), unsafe_allow_html=True)
    with col3:
        st.markdown(stat_card(inactive_count, "Inactive", "stat-card-warm", "gradient-text-warm"), unsafe_allow_html=True)

    divider()

    tab1, tab2 = st.tabs(["👥 All Sub Admins", "➕ Add Sub Admin"])

    with tab1:
        if subadmins:
            for s in subadmins:
                is_active = s.get("is_active", True)
                status_badge = "active" if is_active else "inactive"

                with st.expander(f"👤 {s.get('full_name', 'N/A')}  |  {s.get('email', 'N/A')}  |  {'Active' if is_active else 'Inactive'}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"""
                        <div class="data-card">
                            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:0.85rem;">
                                <div><span style="color:#5a5e73;">Name:</span> <span style="color:#e0e0e0;font-weight:600;">{s.get('full_name', 'N/A')}</span></div>
                                <div><span style="color:#5a5e73;">Email:</span> <span style="color:#e0e0e0;">{s.get('email', 'N/A')}</span></div>
                                <div><span style="color:#5a5e73;">Role:</span> {badge('sub_admin', 'sub')}</div>
                                <div><span style="color:#5a5e73;">Status:</span> {badge(status_badge, status_badge)}</div>
                                <div><span style="color:#5a5e73;">Joined:</span> <span style="color:#e0e0e0;">{s.get('created_at', '')[:10]}</span></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown("#### Actions")
                        if is_active:
                            if st.button("Deactivate", key=f"deact_{s['id']}", use_container_width=True):
                                try:
                                    toggle_sub_admin_active(s["id"], False)
                                    st.success("Sub admin deactivated!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Failed: {e}")
                        else:
                            if st.button("Activate", key=f"act_{s['id']}", use_container_width=True, type="primary"):
                                try:
                                    toggle_sub_admin_active(s["id"], True)
                                    st.success("Sub admin activated!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Failed: {e}")

                        divider()

                        if st.button("Delete Sub Admin", key=f"del_{s['id']}", use_container_width=True):
                            try:
                                delete_sub_admin(s["id"])
                                st.success("Sub admin deleted!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed: {e}")
        else:
            empty_state("👥", "No sub admins found. Add your first sub admin!")

    with tab2:
        st.markdown(f'<div class="section-header">{gradient_text("Add New Sub Admin")}</div>', unsafe_allow_html=True)

        with st.form("add_subadmin_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                sa_name = st.text_input("Full Name", placeholder="e.g. John Doe")
                sa_email = st.text_input("Email", placeholder="e.g. john@traffic.gov")
            with col_b:
                sa_password = st.text_input("Password", type="password", placeholder="Min 6 characters")
                sa_confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")

            submitted = st.form_submit_button("Create Sub Admin", type="primary", use_container_width=True)

            if submitted:
                if not sa_name or not sa_email or not sa_password:
                    st.error("All fields are required")
                elif sa_password != sa_confirm:
                    st.error("Passwords do not match")
                elif len(sa_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    try:
                        create_sub_admin(sa_email, sa_password, sa_name)
                        st.success(f"Sub admin '{sa_name}' created successfully!")
                        st.rerun()
                    except Exception as e:
                        error_msg = str(e)
                        if "already registered" in error_msg.lower():
                            st.error("Email already registered.")
                        else:
                            st.error(f"Failed to create sub admin: {error_msg}")
