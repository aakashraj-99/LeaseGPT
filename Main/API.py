from flask import Flask, request, jsonify, Response
from testprog3 import get_answer
# from flask_cors import CORS, cross_origin

app = Flask(__name__)

# CORS(app)

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    # Change the port to the desired value (e.g., 5000)
    app.run(debug=True, host='0.0.0.0', port=81)

# Define the API endpoint for handling POST requests
@app.route('/get_answer', methods=['POST'])
# @cross_origin()
def post_example():
    try:
        # Assuming the data is sent as JSON
        request_data = request.get_json()
        print(request_data,request_data["Question"])

        # Call the function to process the request data
        result = get_answer(request_data["Question"])
        print(request_data,request_data["Question"])
        
        responsedict = {"Answer": result.response}
        

        # Return the result as JSON
        return jsonify(responsedict)

    except Exception as e:
        # Handle exceptions or errors
        return jsonify({"error": str(e)}), 500

