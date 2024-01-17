from flask import Flask, request, jsonify, Response
from testprog3 import get_answer
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get_answer', methods=['POST'])
def post_example():
    try:
        request_data = request.get_json()
        print("Received POST request:", request_data)

        result = get_answer(request_data["Question"])
        print("Result:", result)

        responsedict = {"Answer": result.response}

        return jsonify(responsedict)

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=81)
