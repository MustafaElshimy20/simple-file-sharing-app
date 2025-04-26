from flask import Flask, render_template, request, redirect
import boto3
import os
from werkzeug.utils import secure_filename

# Configuration
S3_BUCKET = 'file-sharing-app-cloudteam'
S3_REGION = 'eu-north-1'

app = Flask(__name__)
s3 = boto3.client('s3', region_name=S3_REGION)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            s3.upload_fileobj(uploaded_file, S3_BUCKET, filename)
            file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{filename}"
            return f"File uploaded successfully! <a href='{file_url}'>Download {filename}</a>"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
