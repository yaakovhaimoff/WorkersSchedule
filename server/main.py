from flask import Flask, jsonify, json, request

app = Flask(__name__, static_url_path='')

@app.route('/')
def home():  # At the same home function as before
    return app.send_static_file('index.html')  # Return index.html from the static folder

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify(message='Hello from the server!')

# @app.route('/api/uploadFile', methods=['POST'])
# def upload_file():
#     return jsonify(message='File uploaded successfully!')
@app.route('/api/uploadFile', methods=['POST'])
def upload_file():
    # Check if a file was provided in the request
    if 'file' not in request.files:
        return jsonify(message='No file provided'), 400

    file = request.files['file']

    # Check if the file has a valid name and extension
    if file.filename == '':
        return jsonify(message='No selected file'), 400

    # You can access the file contents using file.read()
    file_contents = file.read()

    # Convert the file contents to a string (assuming it's text)
    file_contents_str = file_contents.decode('utf-8')

    # You can then process the file_contents_str as needed
    # For example, if it's JSON data, you can parse it
    try:
        json_data = json.loads(file_contents_str)
        return jsonify(message='File uploaded successfully!', data=json_data)
    except Exception as e:
        return jsonify(message='Failed to parse JSON data', error=str(e)), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
