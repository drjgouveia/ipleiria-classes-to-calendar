from flask import Flask, render_template, request, send_file
import os
from data_handler import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        response = request.form.get('response')
        processed_data = process_data(response)
        if processed_data:
            file_path = create_file(processed_data)
            return send_file(file_path, as_attachment=True, download_name='calendar.ics')

    return render_template('index.html')


def process_data(data):
    json_data = extract_json_from_request_data(data)
    if json_data:
        return convert_to_events(json_data)

    return []


def create_file(cal):
    file_path = 'temp/calendar.ics'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        file.writelines(cal.serialize_iter())
    return file_path


if __name__ == '__main__':
    app.run(debug=True)
