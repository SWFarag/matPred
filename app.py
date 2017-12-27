from flask import Flask, render_template, request, session,make_response, send_file
from flask_security import Security, login_required, SQLAlchemySessionUserDatastore
from database import db_session, init_db
from models import User, Role
from flask_babel import Babel
from flask_mail import Mail
import preloader
import os, StringIO
import pandas as pd


# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_HASH']='bcrypt'
app.config['SECURITY_PASSWORD_SALT']='nothingImportant'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_CONFIRMABLE'] = True

app.config.from_object('config.email')


# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session,                                            User, Role)
security = Security(app, user_datastore)

# Setup mail extension
mail = Mail(app)

# Setup babel
babel = Babel(app)


#instantiate the database
init_db()

###### Pre-loading files #####
path = app.root_path
preloader = preloader.PreLoader(path)

app.config['UPLOAD_FOLDER'] = os.path.join(path, "uploaded/")
app.config['EXTRACTION_FOLDER'] = os.path.join(path, "extracted/")
app.config['ALLOWED_EXTENSIONS'] = set(['sdf','zip','mol'])
if not os.path.exists(app.config['UPLOAD_FOLDER']):os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['EXTRACTION_FOLDER']):os.makedirs(app.config['EXTRACTION_FOLDER'])
##################################### Main ###########################
# Views
@app.route('/')
@login_required
def main():
    return render_template('index.html')

###################################    Predictor  ##############################
@app.route('/Predictor')
def doPrediction():
    # preloader.nrps_parser.deleteUploadedFiles(app.config['UPLOAD_FOLDER'])
    # preloader.nrps_parser.deleteUploadedFiles(app.config['EXTRACTION_FOLDER'])
    return render_template('Predictor/predictor.html')

@app.route('/Predictor/Upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist("file[]")
    filenames_dic, bad_filenames_dic = preloader.predictor.uploadFiles(uploaded_files=uploaded_files, app=app)
    return render_template('Predictor/upload.html', filenames_dic=filenames_dic, bad_filenames_dic=bad_filenames_dic)

@app.route('/Predictor/Predictions')
def getPredictions():
    results = preloader.predictor.modelPrediction(path=app.config['UPLOAD_FOLDER'])
    results.to_csv(os.path.join(app.config['EXTRACTION_FOLDER'], ".csv"), index=False)
    results = preloader.predictor.tohtml_library_parser(results, "extracted_linkers")
    return render_template('Predictor/prediction.html', table=results, title='Predictions')

@app.route('/Predictor/Predictions/Download')
def download_tab():
    extracted_linkers = pd.read_csv(os.path.join(app.config['EXTRACTION_FOLDER'], ".csv"))
    db = extracted_linkers
    s = StringIO.StringIO()
    db.to_csv(s, index=False)
    csv = s.getvalue()
    response = make_response(csv)
    cd = 'attachment; filename=predictions_results.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype ='text/csv'
    return response

################### Nav-Bar ###########
@app.route('/Contact')
def getinfo():
    return render_template("Navbar/personal.html")

@app.route('/Uploads_Examples')
def getuploadExamples():
    return render_template("Navbar/upload_example.html")

@app.route('/Uploads_Examples/Daptomycin_BGC')
def getDaptomycin():
    return send_file(os.path.join(path,'files2Read/templates/Daptomycin.gbk'),  attachment_filename="Daptomycin_BGC.gbk", as_attachment=True)


@app.route('/Uploads_Examples/Vancomycin_BGC')
def getVancomycin():
    return send_file(os.path.join(path,'files2Read/templates/Vancomycin.gbk'), attachment_filename="Vancomycin_BGC.gbk", as_attachment=True)


@app.route('/Tutorial')
def getTutorial():
    return render_template("Navbar/tutorial2.html")

@app.route('/postmethod_3', methods = ['POST', 'GET'])
def get_post_javascript_data3():
    global listOfEdits
    listOfEdits = request.form['javascript_data']
    listOfEdits = ast.literal_eval(listOfEdits)
    return "Done"
if __name__ == '__main__':
    app.run()
