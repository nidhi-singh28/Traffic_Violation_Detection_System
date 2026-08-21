import streamlit as st
from utils.styles import gradient_text, badge, divider, empty_state
from utils.supabase_client import get_challans_by_user


def render():
    user_id = st.session_state.user.id
    profile = st.session_state.profile

    st.markdown(f"""
    <div class="animate-fade-in" style="margin-bottom:24px;">
        <h1 style="margin:0;font-size:2rem;">{gradient_text("My Challans")}</h1>
        <p style="color:#5a5e73;margin:4px 0 0 0;font-size:0.9rem;">Challans issued by you</p>
    </div>
    """, unsafe_allow_html=True)

    challans = get_challans_by_user(user_id)

    status_options = ["All", "pending", "approved", "paid", "disputed"]
    if "my_challans_status_filter" not in st.session_state:
        st.session_state.my_challans_status_filter = "All"
    if st.session_state.my_challans_status_filter not in status_options:
        st.session_state.my_challans_status_filter = "All"

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        status_filter = st.selectbox(
            "Filter by Status",
            status_options,
            format_func=lambda x: x.title(),
            key="my_challans_status_filter",
        )
    with col_f2:
        search = st.text_input("Search Vehicle No.", placeholder="e.g. MH12AB1234")

    if challans:
        filtered = challans
        if status_filter != "All":
            filtered = [c for c in filtered if c.get("status") == status_filter]
        if search:
            filtered = [c for c in filtered if search.upper() in c.get("vehicle_number", "").upper()]

        st.markdown(f'<div style="color:#8b8fa3;font-size:0.85rem;margin:12px 0;">Showing {len(filtered)} of {len(challans)} challans</div>', unsafe_allow_html=True)

        for c in filtered:
            rule_info = c.get("traffic_rules", {}) or {}
            status = c.get("status", "pending")

            with st.expander(
                f"🚗 {c.get('vehicle_number', 'N/A')}  |  ₹{float(c.get('fine_amount', 0)):,.0f}  |  {status.title()}",
                expanded=False,
            ):
                proof_url = c.get("proof_url", "")
                proof_type = str(c.get("proof_type", "") or "").lower()
                if proof_url and ("photo" in proof_type or "image" in proof_type):
                    st.markdown('<div style="margin:6px 0 10px 0;color:#8b8fa3;font-size:0.85rem;">Proof</div>', unsafe_allow_html=True)
                    st.image(proof_url, use_container_width=True)

                st.markdown(f"""
                <div class="data-card animate-slide-in">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                        <div>
                            <span class="vehicle-number">{c.get('vehicle_number', 'N/A')}</span>
                            <span style="color:#5a5e73;margin:0 8px;">|</span>
                            <span style="color:#8b8fa3;font-size:0.85rem;">{rule_info.get('title', 'Unknown')}</span>
                            <span style="color:#5a5e73;margin:0 8px;">|</span>
                            <span class="category-tag">{rule_info.get('category', 'N/A')}</span>
                        </div>
                        <div style="display:flex;align-items:center;gap:12px;">
                            <span class="amount-display">₹{float(c.get('fine_amount', 0)):,.0f}</span>
                            {badge(status, status)}
                        </div>
                    </div>
                    <div style="margin-top:8px;font-size:0.8rem;color:#5a5e73;">
                        Owner: {c.get('owner_name', 'N/A')} | Location: {c.get('location', 'N/A')} | {c.get('created_at', '')[:10]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        empty_state("📋", "You haven't issued any challans yet")
