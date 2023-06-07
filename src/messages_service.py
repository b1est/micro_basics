from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/msg', methods=['GET'])
def get_messages():
    return jsonify(['not implemented yet'])

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port=8000, debug=True)
