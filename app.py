from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os
import pytesseract

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/upload'

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(request.url)
    
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        img = Image.open(filepath)
        text = pytesseract.image_to_string(img)

        return render_template('result.html', text=text, image_path=filepath)
    
if __name__ == '__main__':
    app.run(debug=True)