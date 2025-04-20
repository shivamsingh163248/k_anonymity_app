from flask import Flask, render_template, request, send_file, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

latest_output_file = ""

# def anonymize_data(df):
#     df['Age'] = df['Age'].apply(lambda x: '20-39' if 20 <= x <= 39 else '40+')
#     df['ZIP_Code'] = df['ZIP_Code'].astype(str).str[:3] + '**'
#     return df

def anonymize_data(df):
    df = df.copy()

    # Anonymize Name
    df['Name'] = df['Name'].apply(lambda x: 'Name_' + x[0].upper() + '***')

    # Anonymize Age into buckets
    df['Age'] = df['Age'].apply(lambda x: '18-29' if x <= 29 else ('30-49' if x <= 49 else '50+'))

    # Gender - keeping as-is (or mask if required)
    # df['Gender'] = 'Confidential'  # Optional masking

    # ZIP_Code - keep first 3 digits
    df['ZIP_Code'] = df['ZIP_Code'].astype(str).str[:3] + '**'

    # City - generalize
    df['City'] = df['City'].apply(lambda x: 'City_***')

    # Disease - can keep or hash (keeping as-is for demo)
    # df['Disease'] = df['Disease'].apply(lambda x: hash(x))  # Optional

    # Phone - mask last 5 digits
    df['Phone'] = df['Phone'].astype(str).str[:5] + '*****'

    # Email - mask user part
    df['Email'] = df['Email'].apply(lambda x: 'xxxx' + x[x.find('@'):])

    # Department - generalize
    df['Department'] = df['Department'].apply(lambda x: 'Dept_***')

    # Visit_Date - generalize to month
    df['Visit_Date'] = pd.to_datetime(df['Visit_Date'], errors='coerce').dt.strftime('%Y-%m')

    return df

@app.route('/')
def index():
    return render_template('index.html', preview=None, download_link=None)

@app.route('/upload', methods=['POST'])
def upload():
    global latest_output_file
    file = request.files['file']
    if file.filename.endswith('.csv'):
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        df = pd.read_csv(path)
        anon_df = anonymize_data(df)
        output_path = os.path.join(UPLOAD_FOLDER, 'anonymized_' + file.filename)
        anon_df.to_csv(output_path, index=False)
        latest_output_file = output_path
        preview_data = anon_df.head(10).to_html(classes='table', index=False)
        return render_template('index.html', preview=preview_data, download_link=True)
    return "Invalid file type. Please upload a CSV."

@app.route('/download')
def download():
    global latest_output_file
    return send_file(latest_output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
