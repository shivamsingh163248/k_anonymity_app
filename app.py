from flask import Flask, render_template, request, redirect, send_file, url_for
import pandas as pd
import os
from anonymizer import apply_k_anonymity

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Sample attributes (your dataset headers)
ALL_ATTRIBUTES = ['Name', 'Age', 'Gender', 'ZIP_Code', 'City', 'Disease', 'Phone', 'Email', 'Department', 'Visit_Date']
anonymized_file_path = os.path.join(UPLOAD_FOLDER, 'anonymized_output.csv')


@app.route('/')
def index():
    return render_template('index.html', attributes=ALL_ATTRIBUTES, table_html=None)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    selected_attributes = request.form.getlist('selected_attributes')
    k_value = int(request.form.get('k_value'))

    if not file or not selected_attributes or not k_value:
        return "Please upload a CSV, select attributes, and specify K.", 400

    df = pd.read_csv(file)

    # Apply K-Anonymity
    anonymized_df = apply_k_anonymity(df, selected_attributes, k_value)

    # Save for download
    anonymized_df.to_csv(anonymized_file_path, index=False)

    # Generate HTML table preview
    table_html = anonymized_df.head(10).to_html(classes='table table-striped', index=False)

    return render_template('index.html', attributes=ALL_ATTRIBUTES, table_html=table_html)


@app.route('/download')
def download():
    return send_file(anonymized_file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
