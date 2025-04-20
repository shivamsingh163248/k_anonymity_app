from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def anonymize_data(df):
    df['Age'] = df['Age'].apply(lambda x: '20-39' if 20 <= x <= 39 else '40+')
    df['ZIP_Code'] = df['ZIP_Code'].astype(str).str[:3] + '**'
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file.filename.endswith('.csv'):
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        df = pd.read_csv(path)
        anon_df = anonymize_data(df)
        anon_df.to_csv(path, index=False)
        return send_file(path, as_attachment=True)
    return "Invalid file type. Please upload a CSV."

if __name__ == '__main__':
    app.run(debug=True)
