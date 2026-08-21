"""
Portfolio/demo detection engine.

No YOLO weights, OCR models, external API, or private backend are used here.
The public build intentionally returns clearly-labelled mock results.
"""

from typing import Any, Dict, List
import base64


def detect_violations(file_name: str, file_bytes: bytes, media_type: str) -> Dict[str, Any]:
    if not file_bytes:
        raise ValueError("Uploaded file is empty.")

    if media_type == "video":
        violations = ["Triple Riding"]
    else:
        violations = ["No Helmet"]

    return {
        "detected_violations": [
            {
                "violation": v,
                "vehicle_number": "PB10DEMO01",
                "confidence": "Demo",
                "location": "Demo Location",
                "category": "Safety",
            }
            for v in violations
        ],
        "vehicle_number": "PB10DEMO01",
        "count": len(violations),
        "engine": "mock-demo",
    }


def to_frontend_violations(api_payload: Dict[str, Any], rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rules_by_title = {str(r.get("title", "")).strip().lower(): r for r in (rules or [])}
    mapped = []

    for item in api_payload.get("detected_violations", []) or []:
        name = str(item.get("violation", "Unknown")).strip()
        aliases = {
            "no helmet": "helmet",
            "without helmet": "helmet",
            "helmet": "helmet",
            "triple riding": "triple riding",
            "mobile usage": "mobile usage",
        }
        key = aliases.get(name.lower(), name.lower())
        matched = rules_by_title.get(key)

        mapped.append({
            "violation": name,
            "category": item.get("category", matched.get("category", "General") if matched else "General"),
            "rule_id": matched.get("id") if matched else None,
            "rule_code": matched.get("rule_code", "") if matched else "",
            "fine": float(matched.get("fine_amount", 500)) if matched else 500.0,
            "confidence": item.get("confidence", "Demo"),
            "vehicle_number": item.get("vehicle_number", api_payload.get("vehicle_number", "PB10DEMO01")),
            "owner_name": "Demo Vehicle Owner",
            "location": item.get("location", "Demo Location"),
        })

    return mapped


def as_data_url(file_name: str, file_bytes: bytes) -> str:
    ext = file_name.lower().rsplit(".", 1)[-1] if "." in file_name else "jpg"
    mime = "image/jpeg" if ext in {"jpg", "jpeg"} else "image/png"
    return f"data:{mime};base64,{base64.b64encode(file_bytes).decode('utf-8')}"
