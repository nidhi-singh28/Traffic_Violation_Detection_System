import streamlit as st
from utils.styles import gradient_text, badge, divider, empty_state
from utils.supabase_client import get_all_detections


def render():
    st.markdown(f"""
    <div class="animate-fade-in" style="margin-bottom:24px;">
        <h1 style="margin:0;font-size:2rem;">{gradient_text("Violation Detections")}</h1>
        <p style="color:#5a5e73;margin:4px 0 0 0;font-size:0.9rem;">All violation detection records with proofs</p>
    </div>
    """, unsafe_allow_html=True)

    detections = get_all_detections()

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        status_filter = st.selectbox("Filter by Status", ["All", "processing", "completed", "failed"], format_func=lambda x: x.title())
    with col_f2:
        media_filter = st.selectbox("Filter by Type", ["All", "photo", "video"], format_func=lambda x: x.title() if x != "All" else x)

    if detections:
        filtered = detections
        if status_filter != "All":
            filtered = [d for d in filtered if d.get("status") == status_filter]
        if media_filter != "All":
            filtered = [d for d in filtered if d.get("media_type") == media_filter]

        st.markdown(f'<div style="color:#8b8fa3;font-size:0.85rem;margin:12px 0;">Showing {len(filtered)} of {len(detections)} detections</div>', unsafe_allow_html=True)

        for d in filtered:
            detector = d.get("profiles", {}) or {}
            violations = d.get("detected_violations", [])
            if isinstance(violations, str):
                violations = []
            status = d.get("status", "processing")
            media_type = d.get("media_type", "photo")
            media_url = str(d.get("media_url", "") or "")

            icon = "📷" if media_type == "photo" else "🎥"

            with st.expander(f"{icon} {detector.get('full_name', 'Unknown')}  |  {len(violations)} violation(s)  |  {status.title()}", expanded=False):
                if media_type == "photo" and media_url:
                    st.markdown('<div style="margin:6px 0 10px 0;color:#8b8fa3;font-size:0.85rem;">Proof photo</div>', unsafe_allow_html=True)
                    st.image(media_url, use_container_width=True)

                st.markdown(f"""
                <div class="data-card">
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:0.85rem;">
                        <div><span style="color:#5a5e73;">Uploaded by:</span> <span style="color:#e0e0e0;">{detector.get('full_name', 'N/A')}</span></div>
                        <div><span style="color:#5a5e73;">Email:</span> <span style="color:#e0e0e0;">{detector.get('email', 'N/A')}</span></div>
                        <div><span style="color:#5a5e73;">Media Type:</span> <span style="color:#e0e0e0;">{media_type.title()}</span></div>
                        <div><span style="color:#5a5e73;">Date:</span> <span style="color:#e0e0e0;">{d.get('created_at', '')[:10]}</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if violations:
                    st.markdown(f'<div style="margin:12px 0 8px 0;font-weight:600;color:#e0e0e0;">Detected Violations:</div>', unsafe_allow_html=True)
                    for i, v in enumerate(violations):
                        v_name = v.get("violation", "Unknown") if isinstance(v, dict) else str(v)
                        v_conf = v.get("confidence", "N/A") if isinstance(v, dict) else "N/A"
                        st.markdown(f"""
                        <div class="rule-card" style="padding:12px 16px;margin:4px 0;">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <span style="color:#e0e0e0;font-weight:500;">{i+1}. {v_name}</span>
                                <span style="color:#3a7bd5;font-size:0.8rem;">Confidence: {v_conf}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown('<div style="color:#5a5e73;font-size:0.85rem;">No violations detected in this media</div>', unsafe_allow_html=True)
    else:
        empty_state("🔍", "No violation detections found")
