import json
import sys


def success_envelope(data, warnings=None):
    return {"ok": True, "data": data, "warnings": warnings or []}


def error_envelope(code, message, detail=None):
    return {
        "ok": False,
        "error": {
            "code": code,
            "message": message,
            "detail": detail or {},
        },
    }


def emit_json(payload, stream=None):
    target = stream or sys.stdout
    target.write(json.dumps(payload, ensure_ascii=False, indent=2))
    target.write("\n")
