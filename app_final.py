from flask import Flask, jsonify, request, render_template
import datetime

app = Flask(__name__)

data_sensor = {
    "suhu": 0.0,
    "asap": 0,
    "status": "Normal",
    "last_update": "-"
}

@app.route('/')
def index():
    return render_template('web_interface.html')

@app.route('/update', methods=['POST'])
def update_sensor():
    global data_sensor
    data = request.json

    data_sensor["suhu"] = data.get("suhu", 0.0)
    data_sensor["asap"] = data.get("asap", 0)

    if data_sensor["suhu"] > 30 or data_sensor["asap"] > 600:
        data_sensor["status"] = "Bahaya"
    else:
        data_sensor["status"] = "Normal"

    data_sensor["last_update"] = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return jsonify({"message": "OK"}), 200

@app.route('/api/data')
def api_data():
    return jsonify(data_sensor)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
