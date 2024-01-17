from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

# Specify the upload folder
UPLOAD_FOLDER = '/home/prashant/Documents/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        json_data = request.get_json()
        file_name = request.form.get('file_name')

        # Check if the JSON data is present
        if not json_data:
            return jsonify({'error': 'No JSON data provided'})

        # Save the JSON data to a file in the storage folder
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        with open(file_path, 'w') as file:
            json.dump(json_data, file)

        return jsonify({'message': f'JSON data stored successfully as {file_name}'})
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
