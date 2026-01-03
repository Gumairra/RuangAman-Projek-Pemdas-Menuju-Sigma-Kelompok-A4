from flask import Flask, jsonify, request, render_template
import datetime

app = Flask(__name__)

data_sensor = {
    "suhu" : 0.0,
    "asap" : 0.0,
    "status" : "normal",
    "last_update" : "-",
}

@app.route('/')
def index ():
    return render_template('web-interface.html', sensor=data_sensor)

@app.route('update', methods=['POST'])
def update_sensor():
    global data_sensor
    try:
        content = request.json

        #Mengambil dataJSON dari sensor
        data_sensor["suhu"] = content.get("suhu", data_sensor["suhu"])
        data_sensor["asap"] = content.get("asap", data_sensor["asap"])
        
        if data_sensor["suhu"] > 50 or data_sensor["asap"] > 300:
            data_sensor["status"] = "Bahaya!"
        else:
            data_sensor["status"] = "Normal"
        
        import datetime
        data_sensor["last_update"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return jsonify({"message": "Data Sensor berhasil diterima!"}), 200
    except Exception as e:
        return jsonify({"message": "Terjadi kesalahan dalam memproses data sensor.", "error": str(e)}), 400

#endpoint agar js bisa ambil data terbaru
@app.route('/api/data')
def get_data():
    return jsonify(data_sensor)

if __name__ == '__main__':
    app.run(debug=True, host='0000', port=5000)
