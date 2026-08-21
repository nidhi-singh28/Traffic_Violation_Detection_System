import streamlit as st
from utils.styles import (
    gradient_text, gradient_text_green, gradient_text_gold,
    stat_card, divider, badge
)
from utils.supabase_client import (
    get_user_challan_stats, get_challans_by_user, get_detections_by_user,
    get_traffic_rules
)


def render():
    profile = st.session_state.profile
    user_id = st.session_state.user.id

    def _clickable_stat_card(value, label, card_class, value_class, page, button_key, challan_filter=None):
        st.markdown(
            stat_card(value, label, card_class, value_class, clickable=True),
            unsafe_allow_html=True,
        )
        if st.button("\u200b", key=button_key, use_container_width=True):
            st.session_state.current_page = page
            if challan_filter is not None:
                st.session_state.my_challans_status_filter = challan_filter
            st.rerun()

    st.markdown(f"""
    <div class="animate-fade-in" style="margin-bottom:24px;">
        <h1 style="margin:0;font-size:2rem;">{gradient_text("My Dashboard")}</h1>
        <p style="color:#5a5e73;margin:4px 0 0 0;font-size:0.9rem;">Welcome, {profile.get('full_name', 'Admin')}</p>
    </div>
    """, unsafe_allow_html=True)

    stats = get_user_challan_stats(user_id)
    my_challans = get_challans_by_user(user_id)
    my_detections = get_detections_by_user(user_id)
    rules = get_traffic_rules()

    col1, col2, col3 = st.columns(3)
    with col1:
        _clickable_stat_card(
            stats["total"], "My Challans", "", "gradient-text",
            "challans", "sub_dash_my_challans", "All",
        )
    with col2:
        _clickable_stat_card(
            stats["pending"], "Pending", "stat-card-warm", "gradient-text",
            "challans", "sub_dash_pending", "pending",
        )
    with col3:
        _clickable_stat_card(
            stats["approved"], "Approved", "stat-card-green", "gradient-text-green",
            "challans", "sub_dash_approved", "approved",
        )

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    col4, col5 = st.columns(2)
    with col4:
        st.markdown(stat_card(len(my_detections), "My Detections", "stat-card-warm", "gradient-text"), unsafe_allow_html=True)
    with col5:
        _clickable_stat_card(
            len(rules), "Traffic Rules", "stat-card-green", "gradient-text-green",
            "rules", "sub_dash_traffic_rules",
        )

    divider()

    tab1, tab2 = st.tabs(["📋 My Recent Challans", "🔍 My Recent Detections"])

    with tab1:
        st.markdown(f'<div class="section-header">{gradient_text("My Challans")}</div>', unsafe_allow_html=True)
        if my_challans:
            for c in my_challans[:8]:
                rule_info = c.get("traffic_rules", {}) or {}
                status_class = c.get("status", "pending")
                st.markdown(f"""
                <div class="data-card animate-slide-in">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                        <div>
                            <span class="vehicle-number">{c.get('vehicle_number', 'N/A')}</span>
                            <span style="color:#5a5e73;margin:0 8px;">|</span>
                            <span style="color:#8b8fa3;font-size:0.85rem;">{rule_info.get('title', 'Unknown')}</span>
                        </div>
                        <div style="display:flex;align-items:center;gap:12px;">
                            <span class="amount-display">₹{float(c.get('fine_amount', 0)):,.0f}</span>
                            {badge(status_class, status_class)}
                        </div>
                    </div>
                    <div style="margin-top:8px;font-size:0.8rem;color:#5a5e73;">
                        {c.get('location', 'No location')} | {c.get('created_at', '')[:10]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-state"><div class="empty-state-icon">📋</div>No challans yet. Start detecting violations!</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown(f'<div class="section-header">{gradient_text("My Detections")}</div>', unsafe_allow_html=True)
        if my_detections:
            for d in my_detections[:6]:
                violations = d.get("detected_violations", [])
                if isinstance(violations, str):
                    violations = []
                st.markdown(f"""
                <div class="data-card animate-slide-in">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                        <div>
                            <span style="font-weight:600;color:#e0e0e0;">{d.get('media_type', 'N/A').title()} Upload</span>
                        </div>
                        <div>{badge(d.get('status', 'processing'), d.get('status', 'processing'))}</div>
                    </div>
                    <div style="margin-top:8px;font-size:0.8rem;color:#5a5e73;">
                        {len(violations)} violation(s) detected | {d.get('created_at', '')[:10]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-state"><div class="empty-state-icon">🔍</div>No detections yet</div>', unsafe_allow_html=True)
