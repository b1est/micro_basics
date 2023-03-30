from flask import Flask, jsonify, request

app = Flask(__name__)
messages = {}

@app.route('/log', methods=['POST'])
def post_message():
    msg_id = request.form.get('id')
    msg = request.form.get('msg')
    messages[msg_id] = msg
    print(msg)
    return jsonify({'id': msg_id})

@app.route('/log', methods=['GET'])
def get_messages():
    return jsonify(list(messages.values()))

if __name__ == '__main__':
    app.run(port=8081)
