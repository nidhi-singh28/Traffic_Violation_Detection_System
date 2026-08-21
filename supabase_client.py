"""
Demo data store for the public Traffic VDS portfolio build.

This file intentionally contains NO Supabase connection, API key, password,
or production data. Data lives in Streamlit session state so the demo can run
without an external database.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid
import streamlit as st


SUPER_ID = "00000000-0000-0000-0000-000000000001"
SUB_ID = "00000000-0000-0000-0000-000000000002"


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _uid() -> str:
    return str(uuid.uuid4())


def _store() -> Dict[str, Any]:
    if "_traffic_demo_store" not in st.session_state:
        st.session_state["_traffic_demo_store"] = {
            "profiles": [
                {
                    "id": SUPER_ID,
                    "email": "super@demo.traffic",
                    "full_name": "Demo Super Admin",
                    "role": "super_admin",
                    "is_active": True,
                    "created_at": _now(),
                },
                {
                    "id": SUB_ID,
                    "email": "sub@demo.traffic",
                    "full_name": "Demo Sub Admin",
                    "role": "sub_admin",
                    "is_active": True,
                    "created_at": _now(),
                },
            ],
            "rules": [
                {
                    "id": _uid(), "rule_code": "TR-001", "title": "Helmet",
                    "description": "Helmet not worn while riding.",
                    "fine_amount": 500.0, "category": "Safety",
                    "created_by": SUPER_ID, "created_at": _now(),
                },
                {
                    "id": _uid(), "rule_code": "TR-002", "title": "Triple Riding",
                    "description": "More than two persons on a two-wheeler.",
                    "fine_amount": 1000.0, "category": "Safety",
                    "created_by": SUPER_ID, "created_at": _now(),
                },
                {
                    "id": _uid(), "rule_code": "TR-003", "title": "Mobile Usage",
                    "description": "Using a mobile phone while riding.",
                    "fine_amount": 500.0, "category": "Safety",
                    "created_by": SUPER_ID, "created_at": _now(),
                },
            ],
            "challans": [
                {
                    "id": _uid(), "vehicle_number": "PB10DEMO01",
                    "owner_name": "Demo Vehicle Owner",
                    "rule_id": None, "fine_amount": 500.0,
                    "detected_by": SUB_ID, "proof_url": "",
                    "proof_type": "", "location": "Demo Location",
                    "notes": "Sample portfolio record.", "status": "paid",
                    "approved_by": SUPER_ID, "created_at": _now(),
                },
                {
                    "id": _uid(), "vehicle_number": "DL01DEMO02",
                    "owner_name": "Sample Owner",
                    "rule_id": None, "fine_amount": 1000.0,
                    "detected_by": SUPER_ID, "proof_url": "",
                    "proof_type": "", "location": "Demo Location",
                    "notes": "Sample portfolio record.", "status": "pending",
                    "approved_by": None, "created_at": _now(),
                },
            ],
            "detections": [
                {
                    "id": _uid(), "uploaded_by": SUB_ID, "media_url": "",
                    "media_type": "photo",
                    "detected_violations": [
                        {"violation": "No Helmet", "confidence": "Demo", "vehicle_number": "PB10DEMO01"}
                    ],
                    "status": "completed", "created_at": _now(),
                }
            ],
        }
    return st.session_state["_traffic_demo_store"]


def _profile(pid: str) -> Dict[str, Any]:
    return next((p for p in _store()["profiles"] if p["id"] == pid), {})


def _rule(rule_id: Optional[str]) -> Dict[str, Any]:
    return next((r for r in _store()["rules"] if r["id"] == rule_id), {})


def _enrich_challans(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result = []
    for c in rows:
        item = dict(c)
        item["traffic_rules"] = _rule(c.get("rule_id"))
        item["profiles"] = _profile(c.get("detected_by"))
        result.append(item)
    return result


def _enrich_detections(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result = []
    for d in rows:
        item = dict(d)
        item["profiles"] = _profile(d.get("uploaded_by"))
        result.append(item)
    return result


# --- Demo authentication ---

def _is_demo_credential(email: str, password: str) -> Optional[str]:
    accounts = {
        "admin@traffic-demo.app": ("demo123", "super_admin"),
        "subadmin@traffic-demo.app": ("demo123", "sub_admin"),
    }
    item = accounts.get(str(email).lower().strip())
    return item[1] if item and password == item[0] else None


def _demo_user_id(email: str) -> str:
    return SUPER_ID if email.lower().strip() == "admin@traffic-demo.app" else SUB_ID


def sign_in(email: str, password: str):
    role = _is_demo_credential(email, password)
    if not role:
        raise Exception("Invalid demo credentials")

    uid = _demo_user_id(email)

    class AuthResponse:
        def __init__(self, user_id: str, mail: str):
            self.user = type("User", (), {"id": user_id, "email": mail})()

    return AuthResponse(uid, email.lower().strip())


def sign_out():
    return None


def get_current_session():
    return None


def get_user_profile(user_id: str):
    return _profile(user_id)


# --- Profiles ---

def get_all_profiles():
    return list(_store()["profiles"])


def create_sub_admin(email: str, password: str, full_name: str):
    if any(p["email"].lower() == email.lower() for p in _store()["profiles"]):
        raise Exception("Email already registered")
    profile = {
        "id": _uid(), "email": email, "full_name": full_name,
        "role": "sub_admin", "is_active": True, "created_at": _now(),
    }
    _store()["profiles"].append(profile)
    return profile


def toggle_sub_admin_active(user_id: str, is_active: bool):
    for p in _store()["profiles"]:
        if p["id"] == user_id:
            p["is_active"] = is_active
            return p
    return None


def delete_sub_admin(user_id: str):
    _store()["profiles"][:] = [
        p for p in _store()["profiles"] if p["id"] != user_id
    ]


# --- Traffic rules ---

def get_traffic_rules():
    return list(_store()["rules"])


def create_traffic_rule(rule_code, title, description, fine_amount, category, created_by):
    if any(r["rule_code"].lower() == rule_code.lower() for r in _store()["rules"]):
        raise Exception("duplicate rule code")
    row = {
        "id": _uid(), "rule_code": rule_code, "title": title,
        "description": description, "fine_amount": float(fine_amount),
        "category": category or "General", "created_by": created_by,
        "created_at": _now(),
    }
    _store()["rules"].append(row)
    return row


def update_traffic_rule(rule_id, updates):
    for r in _store()["rules"]:
        if r["id"] == rule_id:
            r.update(updates)
            return r
    return None


def delete_traffic_rule(rule_id):
    _store()["rules"][:] = [r for r in _store()["rules"] if r["id"] != rule_id]


# --- Challans ---

def get_all_challans():
    return _enrich_challans(sorted(_store()["challans"], key=lambda x: x["created_at"], reverse=True))


def get_challans_by_user(user_id):
    rows = [c for c in _store()["challans"] if c.get("detected_by") == user_id]
    return _enrich_challans(sorted(rows, key=lambda x: x["created_at"], reverse=True))


def create_challan(vehicle_number, owner_name, rule_id, fine_amount, detected_by,
                   proof_url="", proof_type="", location="", notes=""):
    row = {
        "id": _uid(), "vehicle_number": vehicle_number,
        "owner_name": owner_name or "Unknown", "rule_id": rule_id or None,
        "fine_amount": float(fine_amount), "detected_by": detected_by,
        "proof_url": proof_url, "proof_type": proof_type,
        "location": location, "notes": notes, "status": "pending",
        "approved_by": None, "created_at": _now(),
    }
    _store()["challans"].insert(0, row)
    return row


def update_challan_status(challan_id, status, approved_by=None):
    for c in _store()["challans"]:
        if c["id"] == challan_id:
            c["status"] = status
            if approved_by:
                c["approved_by"] = approved_by
            return c
    return None


def update_challan_amount(challan_id, fine_amount):
    for c in _store()["challans"]:
        if c["id"] == challan_id:
            c["fine_amount"] = float(fine_amount)
            return c
    return None


# --- Violation detections ---

def get_all_detections():
    return _enrich_detections(sorted(_store()["detections"], key=lambda x: x["created_at"], reverse=True))


def get_detections_by_user(user_id):
    rows = [d for d in _store()["detections"] if d.get("uploaded_by") == user_id]
    return _enrich_detections(sorted(rows, key=lambda x: x["created_at"], reverse=True))


def create_detection(uploaded_by, media_url="", media_type="photo", detected_violations=None):
    row = {
        "id": _uid(), "uploaded_by": uploaded_by, "media_url": media_url,
        "media_type": media_type, "detected_violations": detected_violations or [],
        "status": "completed", "created_at": _now(),
    }
    _store()["detections"].insert(0, row)
    return row


# --- Stats ---

def _compute_stats(challans):
    totals = {
        "total": len(challans), "pending": 0, "approved": 0,
        "paid": 0, "disputed": 0, "total_revenue": 0.0
    }
    for c in challans:
        status = str(c.get("status", "pending")).lower()
        if status in totals:
            totals[status] += 1
        totals["total_revenue"] += float(c.get("fine_amount") or 0)
    return totals


def get_challan_stats():
    return _compute_stats(get_all_challans())


def get_user_challan_stats(user_id):
    t = _compute_stats(get_challans_by_user(user_id))
    return {"total": t["total"], "pending": t["pending"], "approved": t["approved"], "paid": t["paid"]}
