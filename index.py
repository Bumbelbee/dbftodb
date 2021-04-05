from flask import Flask, render_template, request
from werkzeug import secure_filename
import os
import converter



UPLOAD_FOLDER = './uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
   return render_template('index.html')
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      driver = request.form['db_driver']
      f = request.files['file']
      file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
      print(driver)
    #   f.save(file_path)
      
    #   converter.main(file_path,driver)
      return 'file uploaded successfully'
		
if __name__ == '__main__':
   app.run(debug = True)