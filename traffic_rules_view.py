import streamlit as st
from utils.styles import gradient_text, badge, empty_state
from utils.supabase_client import get_traffic_rules


def render():
    st.markdown(f"""
    <div class="animate-fade-in" style="margin-bottom:24px;">
        <h1 style="margin:0;font-size:2rem;">{gradient_text("Traffic Rules")}</h1>
        <p style="color:#5a5e73;margin:4px 0 0 0;font-size:0.9rem;">View traffic rules and fine amounts set by Super Admin</p>
    </div>
    """, unsafe_allow_html=True)

    rules = get_traffic_rules()

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        categories = sorted(list(set(r.get("category", "General") for r in rules))) if rules else []
        category_filter = st.selectbox("Filter by Category", ["All"] + categories)
    with col_f2:
        search = st.text_input("Search Rules", placeholder="Search by title or code...")

    if rules:
        filtered = rules
        if category_filter != "All":
            filtered = [r for r in filtered if r.get("category") == category_filter]
        if search:
            filtered = [r for r in filtered if search.lower() in r.get("title", "").lower() or search.upper() in r.get("rule_code", "").upper()]

        st.markdown(f'<div style="color:#8b8fa3;font-size:0.85rem;margin:12px 0;">Showing {len(filtered)} of {len(rules)} rules</div>', unsafe_allow_html=True)

        for r in filtered:
            st.markdown(f"""
            <div class="rule-card animate-slide-in">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                    <div>
                        <span style="font-weight:700;color:#e0e0e0;font-size:1.05rem;">{r.get('title', 'N/A')}</span>
                        <span class="category-tag" style="margin-left:8px;">{r.get('category', 'General')}</span>
                        <span style="color:#5a5e73;margin-left:8px;font-size:0.8rem;">{r.get('rule_code', '')}</span>
                    </div>
                    <span class="amount-display">₹{float(r.get('fine_amount', 0)):,.0f}</span>
                </div>
                <div style="margin-top:8px;color:#8b8fa3;font-size:0.85rem;">{r.get('description', 'No description')}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        empty_state("📜", "No traffic rules available yet")
