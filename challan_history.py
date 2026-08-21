import re

import streamlit as st
from utils.styles import gradient_text, badge, divider, empty_state
from utils.supabase_client import get_all_challans, update_challan_status, update_challan_amount


def _violation_from_notes(notes: str) -> str:
    if not notes:
        return ""
    m = re.search(r"Auto-generated from detection\s*\(([^)]+)\)", str(notes))
    return m.group(1).strip() if m else ""


def render():
    st.markdown(f"""
    <div class="animate-fade-in" style="margin-bottom:24px;">
        <h1 style="margin:0;font-size:2rem;">{gradient_text("Challan History")}</h1>
        <p style="color:#5a5e73;margin:4px 0 0 0;font-size:0.9rem;">View and manage all challans</p>
    </div>
    """, unsafe_allow_html=True)

    challans = get_all_challans()

    status_options = ["All", "pending", "approved", "paid", "disputed"]
    if "challan_history_status_filter" not in st.session_state:
        st.session_state.challan_history_status_filter = "All"
    if st.session_state.challan_history_status_filter not in status_options:
        st.session_state.challan_history_status_filter = "All"

    col_filter1, col_filter2, col_filter3 = st.columns(3)
    with col_filter1:
        status_filter = st.selectbox(
            "Filter by Status",
            status_options,
            format_func=lambda x: x.title(),
            key="challan_history_status_filter",
        )
    with col_filter2:
        search = st.text_input("Search Vehicle No.", placeholder="e.g. MH12AB1234")
    with col_filter3:
        sort_by = st.selectbox("Sort By", ["Newest First", "Oldest First", "Highest Amount", "Lowest Amount"])

    if challans:
        filtered = challans
        if status_filter != "All":
            filtered = [c for c in filtered if c.get("status") == status_filter]
        if search:
            filtered = [c for c in filtered if search.upper() in c.get("vehicle_number", "").upper()]

        if sort_by == "Oldest First":
            filtered = sorted(filtered, key=lambda x: x.get("created_at", ""))
        elif sort_by == "Highest Amount":
            filtered = sorted(filtered, key=lambda x: float(x.get("fine_amount", 0)), reverse=True)
        elif sort_by == "Lowest Amount":
            filtered = sorted(filtered, key=lambda x: float(x.get("fine_amount", 0)))

        st.markdown(f'<div style="color:#8b8fa3;font-size:0.85rem;margin:12px 0;">Showing {len(filtered)} of {len(challans)} challans</div>', unsafe_allow_html=True)

        for c in filtered:
            rule_info = c.get("traffic_rules", {}) or {}
            detector = c.get("profiles", {}) or {}
            status = c.get("status", "pending")

            notes = c.get("notes") or ""
            violation_label = _violation_from_notes(notes)
            rule_title = rule_info.get("title") or (violation_label if violation_label else "N/A")
            rule_code = rule_info.get("rule_code") or ("—" if violation_label else "N/A")
            rule_cat = rule_info.get("category") or ("General" if violation_label else "N/A")

            with st.expander(f"🚗 {c.get('vehicle_number', 'N/A')}  |  ₹{float(c.get('fine_amount', 0)):,.0f}  |  {status.title()}", expanded=False):
                # Proof preview (photo / data-uri / URL)
                proof_url = str(c.get("proof_url") or "").strip()
                if proof_url.startswith("data:image") or proof_url.startswith("http://") or proof_url.startswith("https://"):
                    st.markdown('<div style="margin:6px 0 10px 0;color:#8b8fa3;font-size:0.85rem;">Proof</div>', unsafe_allow_html=True)
                    st.image(proof_url, use_container_width=True)

                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"""
                    <div class="data-card">
                        <div style="margin-bottom:12px;">
                            <span class="vehicle-number" style="font-size:1.4rem;">{c.get('vehicle_number', 'N/A')}</span>
                        </div>
                        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:0.85rem;">
                            <div><span style="color:#5a5e73;">Owner:</span> <span style="color:#e0e0e0;">{c.get('owner_name', 'N/A')}</span></div>
                            <div><span style="color:#5a5e73;">Rule:</span> <span style="color:#e0e0e0;">{rule_title}</span></div>
                            <div><span style="color:#5a5e73;">Code:</span> <span style="color:#e0e0e0;">{rule_code}</span></div>
                            <div><span style="color:#5a5e73;">Category:</span> <span style="color:#e0e0e0;">{rule_cat}</span></div>
                            <div><span style="color:#5a5e73;">Location:</span> <span style="color:#e0e0e0;">{c.get('location', 'N/A')}</span></div>
                            <div><span style="color:#5a5e73;">Detected by:</span> <span style="color:#e0e0e0;">{detector.get('full_name', 'N/A')}</span></div>
                            <div><span style="color:#5a5e73;">Date:</span> <span style="color:#e0e0e0;">{c.get('created_at', '')[:10]}</span></div>
                            <div><span style="color:#5a5e73;">Proof:</span> <span style="color:#e0e0e0;">{c.get('proof_type', 'None').title()}</span></div>
                        </div>
                        {f'<div style="margin-top:8px;font-size:0.8rem;color:#5a5e73;">Notes: {c.get("notes", "")}</div>' if c.get('notes') else ''}
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f'<div style="text-align:center;padding:8px 0;">{badge(status, status)}</div>', unsafe_allow_html=True)

                    new_amount = st.number_input("Fine Amount", value=float(c.get("fine_amount", 0)), min_value=0.0, key=f"amt_{c['id']}")
                    if st.button("Update Amount", key=f"upd_amt_{c['id']}"):
                        try:
                            update_challan_amount(c["id"], new_amount)
                            st.success("Amount updated!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed: {e}")

                    divider()

                    new_status = st.selectbox("Change Status", ["pending", "approved", "paid", "disputed"], index=["pending", "approved", "paid", "disputed"].index(status), key=f"sts_{c['id']}")
                    if st.button("Update Status", key=f"upd_sts_{c['id']}"):
                        try:
                            update_challan_status(c["id"], new_status, st.session_state.user.id)
                            st.success("Status updated!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed: {e}")
    else:
        empty_state("📋", "No challans found in the system")
