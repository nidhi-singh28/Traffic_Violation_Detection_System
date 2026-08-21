import streamlit as st
from utils.styles import (
    gradient_text, gradient_text_warm, gradient_text_green,
    gradient_text_gold, stat_card, divider, badge
)
from utils.supabase_client import (
    get_challan_stats, get_all_challans, get_all_profiles,
    get_traffic_rules, get_all_detections
)


def render():
    profile = st.session_state.profile

    def _clickable_stat_card(value, label, card_class, value_class, page, button_key, challan_filter=None):
        st.markdown(
            stat_card(value, label, card_class, value_class, clickable=True),
            unsafe_allow_html=True,
        )
        if st.button("\u200b", key=button_key, use_container_width=True):
            st.session_state.current_page = page
            if challan_filter is not None:
                st.session_state.challan_history_status_filter = challan_filter
            st.rerun()

    st.markdown(f"""
    <div class="animate-fade-in" style="margin-bottom:24px;">
        <h1 style="margin:0;font-size:2rem;">{gradient_text("Super Admin Dashboard")}</h1>
        <p style="color:#5a5e73;margin:4px 0 0 0;font-size:0.9rem;">Welcome back, {profile.get('full_name', 'Admin')}</p>
    </div>
    """, unsafe_allow_html=True)

    stats = get_challan_stats()
    subadmins = get_all_profiles()
    rules = get_traffic_rules()
    detections = get_all_detections()
    sub_admin_count = len([s for s in subadmins if s.get("role") == "sub_admin"])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        _clickable_stat_card(
            stats["total"], "Total Challans", "", "gradient-text",
            "challans", "dash_nav_total_challans", "All",
        )
    with col2:
        _clickable_stat_card(
            stats["pending"], "Pending", "stat-card-warm", "gradient-text-warm",
            "challans", "dash_nav_pending", "pending",
        )
    with col3:
        _clickable_stat_card(
            stats["paid"], "Paid", "stat-card-green", "gradient-text-green",
            "challans", "dash_nav_paid", "paid",
        )
    with col4:
        st.markdown(stat_card(f"₹{stats['total_revenue']:,.0f}", "Revenue", "stat-card-gold", "gradient-text-gold"), unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    col5, col6, col7 = st.columns(3)
    with col5:
        _clickable_stat_card(
            sub_admin_count, "Sub Admins", "", "gradient-text",
            "subadmins", "dash_nav_sub_admins",
        )
    with col6:
        _clickable_stat_card(
            len(rules), "Traffic Rules", "stat-card-green", "gradient-text-green",
            "rules", "dash_nav_traffic_rules",
        )
    with col7:
        st.markdown(stat_card(len(detections), "Detections", "stat-card-warm", "gradient-text-warm"), unsafe_allow_html=True)

    divider()

    tab1, tab2, tab3 = st.tabs(["📋 Recent Challans", "🔍 Recent Detections", "📊 Overview"])

    with tab1:
        st.markdown(f'<div class="section-header">{gradient_text("Recent Challans")}</div>', unsafe_allow_html=True)
        challans = get_all_challans()
        if challans:
            for c in challans[:8]:
                rule_info = c.get("traffic_rules", {}) or {}
                detector = c.get("profiles", {}) or {}
                status_class = c.get("status", "pending")
                st.markdown(f"""
                <div class="data-card animate-slide-in">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                        <div>
                            <span class="vehicle-number">{c.get('vehicle_number', 'N/A')}</span>
                            <span style="color:#5a5e73;margin:0 8px;">|</span>
                            <span style="color:#8b8fa3;font-size:0.85rem;">{rule_info.get('title', 'Unknown Rule')}</span>
                        </div>
                        <div style="display:flex;align-items:center;gap:12px;">
                            <span class="amount-display">₹{float(c.get('fine_amount', 0)):,.0f}</span>
                            {badge(status_class, status_class)}
                        </div>
                    </div>
                    <div style="margin-top:8px;font-size:0.8rem;color:#5a5e73;">
                        Detected by: {detector.get('full_name', 'Unknown')} | {c.get('created_at', '')[:10]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-state"><div class="empty-state-icon">📋</div>No challans found</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown(f'<div class="section-header">{gradient_text("Recent Detections")}</div>', unsafe_allow_html=True)
        if detections:
            for d in detections[:6]:
                detector = d.get("profiles", {}) or {}
                violations = d.get("detected_violations", [])
                if isinstance(violations, str):
                    violations = []
                st.markdown(f"""
                <div class="data-card animate-slide-in">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                        <div>
                            <span style="font-weight:600;color:#e0e0e0;">{detector.get('full_name', 'Unknown')}</span>
                            <span style="color:#5a5e73;margin:0 8px;">|</span>
                            <span style="color:#8b8fa3;font-size:0.85rem;">{d.get('media_type', 'N/A').title()}</span>
                        </div>
                        <div>{badge(d.get('status', 'processing'), d.get('status', 'processing'))}</div>
                    </div>
                    <div style="margin-top:8px;font-size:0.8rem;color:#5a5e73;">
                        {len(violations)} violation(s) detected | {d.get('created_at', '')[:10]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-state"><div class="empty-state-icon">🔍</div>No detections found</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown(f'<div class="section-header">{gradient_text("Overview")}</div>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
            <div class="stat-card animate-fade-in">
                <div class="stat-label">Challan Status Breakdown</div>
                <div class="divider-glow"></div>
                <div style="text-align:left;padding:8px 0;">
                    <div style="display:flex;justify-content:space-between;padding:6px 0;">
                        <span style="color:#ffc107;">Pending</span>
                        <span style="font-weight:700;color:#ffc107;">{stats['pending']}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;padding:6px 0;">
                        <span style="color:#28a745;">Approved</span>
                        <span style="font-weight:700;color:#28a745;">{stats['approved']}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;padding:6px 0;">
                        <span style="color:#00d2ff;">Paid</span>
                        <span style="font-weight:700;color:#00d2ff;">{stats['paid']}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;padding:6px 0;">
                        <span style="color:#f5576c;">Disputed</span>
                        <span style="font-weight:700;color:#f5576c;">{stats['disputed']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
            <div class="stat-card animate-fade-in">
                <div class="stat-label">Quick Stats</div>
                <div class="divider-glow"></div>
                <div style="text-align:left;padding:8px 0;">
                    <div style="display:flex;justify-content:space-between;padding:6px 0;">
                        <span style="color:#8b8fa3;">Total Rules</span>
                        <span style="font-weight:700;color:#e0e0e0;">{len(rules)}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;padding:6px 0;">
                        <span style="color:#8b8fa3;">Active Sub Admins</span>
                        <span style="font-weight:700;color:#e0e0e0;">{sub_admin_count}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;padding:6px 0;">
                        <span style="color:#8b8fa3;">Total Detections</span>
                        <span style="font-weight:700;color:#e0e0e0;">{len(detections)}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;padding:6px 0;">
                        <span style="color:#8b8fa3;">Total Revenue</span>
                        <span class="amount-display">₹{stats['total_revenue']:,.0f}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
