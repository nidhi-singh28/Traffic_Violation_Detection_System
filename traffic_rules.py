import streamlit as st
from utils.styles import gradient_text, gradient_text_green, badge, divider, empty_state
from utils.supabase_client import (
    get_traffic_rules, create_traffic_rule, update_traffic_rule, delete_traffic_rule
)


def render():
    st.markdown(f"""
    <div class="animate-fade-in" style="margin-bottom:24px;">
        <h1 style="margin:0;font-size:2rem;">{gradient_text("Traffic Rules")}</h1>
        <p style="color:#5a5e73;margin:4px 0 0 0;font-size:0.9rem;">Add, edit, and manage traffic rules and fine amounts</p>
    </div>
    """, unsafe_allow_html=True)

    user_id = st.session_state.user.id
    rules = get_traffic_rules()

    tab1, tab2 = st.tabs(["📜 All Rules", "➕ Add New Rule"])

    with tab1:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            category_filter = st.selectbox("Filter by Category", ["All"] + sorted(list(set(r.get("category", "General") for r in rules))) if rules else ["All"])
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
                with st.expander(f"📜 {r.get('rule_code', 'N/A')}  |  {r.get('title', 'N/A')}  |  ₹{float(r.get('fine_amount', 0)):,.0f}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"""
                        <div class="rule-card">
                            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                                <div>
                                    <span style="font-weight:700;color:#e0e0e0;font-size:1.1rem;">{r.get('title', 'N/A')}</span>
                                    <span class="category-tag" style="margin-left:8px;">{r.get('category', 'General')}</span>
                                </div>
                                <span class="amount-display" style="font-size:1.5rem;">₹{float(r.get('fine_amount', 0)):,.0f}</span>
                            </div>
                            <div style="color:#8b8fa3;font-size:0.85rem;">{r.get('description', 'No description')}</div>
                            <div style="margin-top:8px;font-size:0.75rem;color:#5a5e73;">Code: {r.get('rule_code', 'N/A')} | Created: {r.get('created_at', '')[:10]}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown("#### Edit Rule")
                        new_title = st.text_input("Title", value=r.get("title", ""), key=f"title_{r['id']}")
                        new_desc = st.text_area("Description", value=r.get("description", ""), key=f"desc_{r['id']}", height=80)
                        new_amount = st.number_input("Fine Amount", value=float(r.get("fine_amount", 0)), min_value=0.0, key=f"amount_{r['id']}")
                        new_category = st.text_input("Category", value=r.get("category", "General"), key=f"cat_{r['id']}")

                        if st.button("Update Rule", key=f"upd_{r['id']}", type="primary"):
                            try:
                                update_traffic_rule(r["id"], {
                                    "title": new_title,
                                    "description": new_desc,
                                    "fine_amount": new_amount,
                                    "category": new_category,
                                })
                                st.success("Rule updated!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed: {e}")

                        divider()

                        if st.button("Delete Rule", key=f"del_{r['id']}", type="secondary"):
                            try:
                                delete_traffic_rule(r["id"])
                                st.success("Rule deleted!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed: {e}")
        else:
            empty_state("📜", "No traffic rules found. Add your first rule!")

    with tab2:
        st.markdown(f'<div class="section-header">{gradient_text("Add New Traffic Rule")}</div>', unsafe_allow_html=True)

        with st.form("add_rule_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                rule_code = st.text_input("Rule Code", placeholder="e.g. R001")
                title = st.text_input("Title", placeholder="e.g. Overspeeding")
                category = st.text_input("Category", placeholder="e.g. Speed, Parking, Signal")
            with col_b:
                fine_amount = st.number_input("Fine Amount (₹)", min_value=0.0, value=500.0, step=100.0)
                description = st.text_area("Description", placeholder="Describe the traffic rule...", height=120)

            submitted = st.form_submit_button("Add Rule", type="primary", use_container_width=True)

            if submitted:
                if not rule_code or not title:
                    st.error("Rule code and title are required")
                else:
                    try:
                        create_traffic_rule(rule_code, title, description, fine_amount, category, user_id)
                        st.success(f"Rule '{title}' added successfully!")
                        st.rerun()
                    except Exception as e:
                        if "unique" in str(e).lower() or "duplicate" in str(e).lower():
                            st.error("Rule code already exists. Use a different code.")
                        else:
                            st.error(f"Failed to add rule: {e}")
