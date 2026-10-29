from flask import Flask, render_template, request, jsonify, send_from_directory
from calculator.engine import calculate
from calculator.equations import solve_equation
from calculator.matrices import matrix_operation
from calculator.conversions import convert_units
from calculator.statistics import summarize
from calculator.vectors import vector_operation
from calculator.number_systems import convert_base
from calculator.validation import APIError

import os

ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(ROOT, "templates"), static_folder=os.path.join(ROOT, "static"))
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/manifest.webmanifest")
def manifest():
    return send_from_directory(app.static_folder, "manifest.webmanifest", mimetype="application/manifest+json")

@app.get("/service-worker.js")
def service_worker():
    response = send_from_directory(app.static_folder, "service-worker.js", mimetype="application/javascript")
    response.headers["Service-Worker-Allowed"] = "/"
    response.headers["Cache-Control"] = "no-cache"
    return response

@app.get("/api/health")
def health():
    return jsonify({"ok": True, "name": "CW Engineering"})

@app.post("/api/calculate")
def api_calculate():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("expression"), str):
        return jsonify({"ok": False, "error": "Send JSON with an expression string."}), 400
    try:
        result = calculate(data["expression"], angle_mode=data.get("angle_mode", "DEG"), precision=data.get("precision", 10))
        return jsonify({"ok": True, **result})
    except (ValueError, ZeroDivisionError, TypeError) as exc:
        return jsonify({"ok": False, "error": str(exc) or "Invalid calculation."}), 400
    except Exception:
        app.logger.exception("Calculation failed")
        return jsonify({"ok": False, "error": "Calculation could not be completed."}), 400

@app.post("/api/equation")
def api_equation():
    data = request.get_json(silent=True) or {}
    try:
        return jsonify({"ok": True, "solutions": solve_equation(data.get("equation", ""), data.get("variable", "x"))})
    except (ValueError, TypeError) as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

@app.post("/api/matrix")
def api_matrix():
    data = request.get_json(silent=True) or {}
    try:
        return jsonify({"ok": True, "result": matrix_operation(data.get("operation"), data.get("a"), data.get("b"))})
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

@app.post("/api/convert")
def api_convert():
    data = request.get_json(silent=True) or {}
    try:
        return jsonify({"ok": True, "value": convert_units(data.get("value"), data.get("from_unit"), data.get("to_unit"))})
    except (ValueError, TypeError) as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

@app.post("/api/statistics")
def api_statistics():
    data = request.get_json(silent=True) or {}
    try:
        return jsonify({"ok": True, "result": summarize(data.get("values", []))})
    except (ValueError, TypeError) as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

@app.post("/api/vector")
def api_vector():
    data = request.get_json(silent=True) or {}
    try:
        return jsonify({"ok": True, "result": vector_operation(data.get("operation"), data.get("a"), data.get("b"))})
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

@app.post("/api/base")
def api_base():
    data = request.get_json(silent=True) or {}
    try:
        return jsonify({"ok": True, "result": convert_base(data.get("value"), data.get("from_base"), data.get("to_base"))})
    except (ValueError, TypeError) as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400


def _serve():
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False, threaded=True)


def start_server():
    """Start the local calculator web server and wait until it responds."""
    import threading, time, urllib.request
    thread = threading.Thread(target=_serve, name="CWFlaskServer", daemon=True)
    thread.start()
    url = "http://127.0.0.1:5000/api/health"
    deadline = time.time() + 20
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return True
        except Exception:
            time.sleep(0.25)
    raise RuntimeError("CW Engineering local server failed to start")
