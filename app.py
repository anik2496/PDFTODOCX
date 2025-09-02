from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from pdf2docx import Converter
from docx2pdf import convert as docx2pdf_convert

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_file():
    uploaded_file = request.files['file']
    convert_type = request.form['convert_type']

    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(input_path)

        if convert_type == 'pdf_to_docx' and filename.endswith('.pdf'):
            output_path = input_path.replace('.pdf', '.docx')
            cv = Converter(input_path)
            cv.convert(output_path)
            cv.close()
            return send_file(output_path, as_attachment=True)

        elif convert_type == 'docx_to_pdf' and filename.endswith('.docx'):
            output_path = input_path.replace('.docx', '.pdf')
            docx2pdf_convert(input_path, output_path)
            return send_file(output_path, as_attachment=True)

        else:
            return "Invalid file type or conversion", 400

    return "No file uploaded", 400

if __name__ == '__main__':
    app.run(debug=True)

