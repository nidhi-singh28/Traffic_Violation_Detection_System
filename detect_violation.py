import streamlit as st
from utils.styles import gradient_text, empty_state, badge
from utils.supabase_client import (
    create_detection,
    create_challan,
    get_traffic_rules
)
from utils.backend_api import (
    detect_violations,
    to_frontend_violations,
    as_data_url,
)


def render():

    profile = st.session_state.profile
    user_id = st.session_state.user.id

    st.markdown(
        f"""
        <h1>{gradient_text("Detect Violation")}</h1>
        <p style="color:#5a5e73;">
        Upload photo or video to detect traffic violations
        </p>
        """,
        unsafe_allow_html=True
    )

    rules = get_traffic_rules()

    st.info("🎭 **Portfolio Demo Mode:** detection results are simulated. Private YOLO weights, OCR models, and production services are not included in this public build.")

    tab1, tab2 = st.tabs(["📷 Upload & Detect", "📋 Create Challan Manually"])

    # ==========================
    # TAB 1 - REAL BACKEND ONLY
    # ==========================
    with tab1:
        if "last_detection" not in st.session_state:
            st.session_state.last_detection = None

        media_type = st.radio(
            "Media Type",
            ["photo", "video"],
            horizontal=True
        )

        uploaded_file = st.file_uploader(
            "Choose file",
            type=["jpg", "jpeg", "png", "mp4", "avi", "mov"]
        )

        if st.button("🔍 Detect Violations", type="primary"):

            if not uploaded_file:
                st.error("Please upload a file.")
                return

            try:
                uploaded_file.seek(0)
                file_bytes = uploaded_file.read()

                if not file_bytes:
                    st.error("File is empty.")
                    return

                # 🔥 REAL API CALL
                api_result = detect_violations(
                    uploaded_file.name,
                    file_bytes,
                    media_type
                )

                violations = to_frontend_violations(api_result, rules)
                detected_plate = (
                    str(api_result.get("vehicle_number") or "UNKNOWN")
                    if isinstance(api_result, dict)
                    else "UNKNOWN"
                )

                proof_url = as_data_url(uploaded_file.name, file_bytes) if media_type == "photo" else ""

                st.session_state.last_detection = {
                    "api_result": api_result,
                    "violations": violations,
                    "detected_plate": detected_plate,
                    "media_name": uploaded_file.name,
                    "media_type": media_type,
                    "proof_url": proof_url,
                }

                # Save detection in DB
                create_detection(
                    uploaded_by=user_id,
                    media_url=proof_url if proof_url else uploaded_file.name,
                    media_type=media_type,
                    detected_violations=violations,
                )

            except Exception as e:
                st.error(f"Backend connection failed: {e}")
                return

        # Render last detection result outside detect-click branch,
        # so Generate Challan button works on subsequent reruns.
        last_detection = st.session_state.get("last_detection")
        if last_detection:
            violations = last_detection.get("violations", []) or []
            detected_plate = str(last_detection.get("detected_plate") or "UNKNOWN")
            media_type_for_challan = str(last_detection.get("media_type") or "photo")
            proof_url_for_challan = str(last_detection.get("proof_url") or "")

            st.markdown(
                f"""
                <div class="stat-card stat-card-green animate-fade-in" style="margin-bottom:14px;">
                    <div class="stat-label">DETECTION COMPLETE</div>
                    <div class="stat-number">{len(violations)}</div>
                    <div class="stat-label">VIOLATIONS FOUND</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="data-card animate-fade-in" style="margin-bottom:18px;">
                    <div style="color:#8b8fa3;font-size:0.85rem;">Detected vehicle plate</div>
                    <div class="vehicle-number" style="margin-top:10px;font-size:1.5rem;">{detected_plate}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if proof_url_for_challan and media_type_for_challan == "photo":
                st.image(proof_url_for_challan, caption="Proof photo", use_container_width=True)

            if violations:
                for i, v in enumerate(violations):
                    v_name = v.get("violation", "Unknown")
                    v_location = v.get("location", "Auto-detected")
                    v_conf = v.get("confidence", "N/A")
                    plate_for_ui = detected_plate if detected_plate else v.get("vehicle_number", "UNKNOWN")

                    st.markdown(
                        f"""
                        <div class="rule-card animate-slide-in" style="margin-top:{12 if i > 0 else 0}px;">
                            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:14px;">
                                <div>
                                    <div style="font-size:1.05rem;font-weight:800;color:#e0e0e0;">
                                        {v_name}
                                    </div>
                                    <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;">
                                        {badge("AUTO DETECTED" if str(v_location).lower().find("auto") != -1 else "DETECTED", badge_type="approved")}
                                        <span style="color:#8b8fa3;font-size:0.85rem;">Confidence: {v_conf}</span>
                                    </div>
                                </div>
                                <div style="text-align:right;">
                                    <div class="vehicle-number">{plate_for_ui}</div>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                empty_state("🔍", "No violations detected in this media")

            st.success("Detection record saved successfully.")
            st.divider()

            if st.button("🧾 Generate Challan", disabled=not bool(violations), use_container_width=True):
                try:
                    for v in violations:
                        create_challan(
                            vehicle_number=str(detected_plate or "UNKNOWN"),
                            owner_name=str(v.get("owner_name") or "Unknown"),
                            rule_id=v.get("rule_id") or "",
                            fine_amount=float(v.get("fine", 500) or 500),
                            detected_by=user_id,
                            proof_url=proof_url_for_challan,
                            proof_type=media_type_for_challan,
                            location=str(v.get("location") or "Auto-detected"),
                            notes=f"Auto-generated from detection ({v.get('violation', 'Unknown')}).",
                        )
                    st.success("Challan generated and saved successfully.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to generate challan: {e}")

    # ==========================
    # TAB 2 - MANUAL CHALLAN
    # ==========================
    with tab2:

        if not rules:
            empty_state("📜", "No traffic rules available.")
            return

        with st.form("manual_form"):

            vehicle_number = st.text_input("Vehicle Number")
            owner_name = st.text_input("Owner Name")

            rule_options = {
                f"{r['rule_code']} - {r['title']}":
                r["id"] for r in rules
            }

            selected_rule = st.selectbox(
                "Violation Rule",
                list(rule_options.keys())
            )

            fine_amount = st.number_input(
                "Fine Amount",
                min_value=0.0,
                step=100.0
            )

            submitted = st.form_submit_button("Create Challan")

            if submitted:

                if not vehicle_number:
                    st.error("Vehicle number required")
                    return

                try:
                    create_challan(
                        vehicle_number=vehicle_number.upper(),
                        owner_name=owner_name,
                        rule_id=rule_options[selected_rule],
                        fine_amount=fine_amount,
                        detected_by=user_id,
                        proof_url="",
                        proof_type="",
                        location="Manual Entry",
                        notes=""
                    )

                    st.success("Challan Created Successfully!")
                    st.rerun()

                except Exception as e:
                    st.error(f"Failed: {e}")