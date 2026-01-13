from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
import datetime

# =========================
# INIT APP
# =========================
app = Flask(__name__)
app.config["SECRET_KEY"] = "ruangaman-secret"

# Socket.IO (wajib untuk endpoint /socket.io)
socketio = SocketIO(app, cors_allowed_origins="*")

# =========================
# STATE (DATA SENSOR + KONTROL)
# =========================
data_sensor = {
    "temperature": 0.0,
    "smoke": 0,
    "status": "Normal",
    "last_update": "-"
}

control_state = {
    "target_temp": 28.0,
    "mode_auto": True,
    "kipas_manual": False
}

# =========================
# ROUTES
# =========================
@app.route("/")
def index():
    return render_template("web_interface.html")


@app.route("/api/data")
def api_data():
    # Data awal untuk page load
    return jsonify({**data_sensor, **control_state})


@app.route("/update", methods=["POST"])
def update_sensor():
    """
    Dipanggil oleh kode sensor di Raspberry Pi.
    Bisa menerima key:
      { "suhu": 31.2, "asap": 650 }
    atau:
      { "temperature": 31.2, "smoke": 650 }
    """
    data = request.get_json(silent=True) or {}

    suhu = data.get("suhu", data.get("temperature", 0.0))
    asap = data.get("asap", data.get("smoke", 0))

    try:
        suhu = float(suhu)
    except Exception:
        suhu = 0.0

    try:
        asap = int(asap)
    except Exception:
        asap = 0

    data_sensor["temperature"] = suhu
    data_sensor["smoke"] = asap

    # status bahaya
    if suhu > 30 or asap > 600:
        data_sensor["status"] = "Bahaya"
    else:
        data_sensor["status"] = "Normal"

    data_sensor["last_update"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # broadcast ke semua browser yang terkoneksi
    socketio.emit("update_data", {**data_sensor, **control_state})

    return jsonify({"message": "OK"}), 200


# =========================
# CONTROL API (dipanggil dari web)
# =========================
@app.route("/api/set_mode", methods=["POST"])
def set_mode():
    data = request.get_json(silent=True) or {}
    control_state["mode_auto"] = bool(data.get("auto", True))

    # jika kembali ke auto, manual fan dimatikan
    if control_state["mode_auto"]:
        control_state["kipas_manual"] = False

    socketio.emit("update_data", {**data_sensor, **control_state})
    return jsonify({"message": "OK"}), 200


@app.route("/api/set_kipas", methods=["POST"])
def set_kipas():
    data = request.get_json(silent=True) or {}

    # hanya berlaku jika mode manual
    if not control_state["mode_auto"]:
        control_state["kipas_manual"] = bool(data.get("on", False))

    socketio.emit("update_data", {**data_sensor, **control_state})
    return jsonify({"message": "OK"}), 200


@app.route("/api/set_target", methods=["POST"])
def set_target():
    data = request.get_json(silent=True) or {}
    try:
        control_state["target_temp"] = float(data.get("target", 28.0))
    except Exception:
        control_state["target_temp"] = 28.0

    socketio.emit("update_data", {**data_sensor, **control_state})
    return jsonify({"message": "OK"}), 200


# =========================
# RUN
# =========================
if __name__ == "__main__":
    # use_reloader=False agar tidak dobel proses saat debug
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)