#-*- coding=utf-8 -*-
import os,shutil
import time,hashlib
import pickle
import face_recognition
from flask import Flask,request,g,jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from handler.hd_base import require

UPLOAD_FOLDER = 'pictures'
API_KEY = 'pre_key'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['SECRET_KEY']  = 'never ever'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/facepath'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_file_name():
	ticks = time.time()
	return hashlib.md5(str(ticks)).hexdigest()

def generate_encodings(filePath):
	image = face_recognition.load_image_file(filePath)
	encodings = face_recognition.face_encodings(image)
	if encodings == []:
		return None
	return encodings[0]


def save_encodings(filePath,encodings):
	f = open(filePath,'wb')
	pickle.dump(encodings,f)
	f.close()

class User(db.Model):
	__tablename__ = 'users'
	id  = db.Column(db.Integer,primary_key = True)
	path = db.Column(db.String(64))
    #face_token = db.Column(db.String(32), primary_key = True)
    #image = db.Column(db.LargeBinary)
    #face_set_token = db.Column(db.String(32), index = True)

	def generate_token(self, expiration = 30*24*3600):
		s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
		return s.dumps({'id': self.id}).decode('ascii')

	@staticmethod
	def verify_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None
		except BadSignature:
			return None

		return User.query.get(data["id"])

	def __repr__(self):
		return "the instance of class User"	   


@app.route('/detect',methods=['POST'])
#@require()
def detect():
    key = request.form['api_key']
    if not key == API_KEY:
    	return None

    file = request.files['image_file']
    #if not file or not allowed_file(file.filename):
    	#return None

    #filename = secure_filename(file.filename)
    filename = generate_file_name() + ".jpg"
    path = os.path.join(app.root_path,app.config['UPLOAD_FOLDER'],filename)
    file.save(path)

    #filename = generate_file_name() + ".txt"
    #path = os.path.join(app.root_path,app.config['UPLOAD_FOLDER'],filename)

    
    user = User(path = path)
    db.session.add(user)
    db.session.commit()

    token = ""
    result = User.query.filter_by(path = path).first()
    if result:
    	g.user = result
    	token = g.user.generate_token()
    
    image = face_recognition.load_image_file(path)
    face_locations = face_recognition.face_locations(image)
    faces = []
    for face_location in face_locations:
    	top, right, bottom, left = face_location
    	face_retangle = {
        	"width" : right - left,
        	"top"   : top,
        	"left"  : left,
        	"height": bottom - top
    	}

    	detect = {
    		"face_retangle": face_retangle,
    		"face_token"   : token
    	}

        faces.append(detect)
    
    re = {
    	"faces":faces
    }
    return jsonify(re)


@app.route('/create',methods = ['POST'])
def create_set():
	key = request.form["api_key"]
	if not key == API_KEY:
		return None

	dirPath = os.path.join(app.root_path,app.config['UPLOAD_FOLDER'],generate_file_name())

	if not os.path.exists(dirPath):
		os.mkdir(dirPath)

	user = User(path = dirPath)
	db.session.add(user)
	db.session.commit()

	result = User.query.filter_by(path = dirPath).first()
	g.user = result
	token = g.user.generate_token()

	return jsonify({"faceset_token" : token})

@app.route('/addface',methods = ['POST'])
def add_face():
	key = request.form["api_key"]
	if not key == API_KEY:
		return None

	face_token  = request.form["face_token"]
	faceset_token = request.form["faceset_token"]

	face_user = User.verify_token(face_token)
	if not face_user:
		return None

	faceset_user = User.verify_token(faceset_token)
	if not faceset_user:
		return None

	filename = os.path.basename(face_user.path)
	newPath = os.path.join(faceset_user.path,filename)
	shutil.move(face_user.path,newPath)

	face_user.path = newPath
	db.session.add(face_user)
	db.session.commit()

	return jsonify({"face_added":1})


@app.route('/removeface',methods = ['POST'])
def delete_face():
	key = request.form['api_key']
	if not key == API_KEY:
		return None

	face_token  = request.form["face_token"]
	faceset_token = request.form["faceset_token"]

	face_user = User.verify_token(face_token)
	if not face_user:
		return None

	path = face_user.path
	os.remove(path)

	db.session.delete(face_user)
	db.session.commit()

	return jsonify({"face_removed":1})


@app.route('/search',methods = ['POST'])
def search_face():
	key = request.form['api_key']
	if not key == API_KEY:
		return None
    
	faceset_token = request.form["faceset_token"]
	faceset_user = User.verify_token(faceset_token)
	if not faceset_token:
		return None

	image = request.files["image_file"]
	if not image or not allowed_file(image.filename):
		return None

	imagePath = os.path.join(app.root_path,"test.jpg")
	image.save(imagePath)
	verifyImage = face_recognition.load_image_file(imagePath)
	verifyImage_encoding = face_recognition.face_encodings(verifyImage)
	if verifyImage_encoding == []:
		return jsonify({"confidence":0})

	re  = []
	dirPath = faceset_user.path;
	files = os.listdir(dirPath)
	for file in files:
		if not os.path.isdir(file):
			path = os.path.join(dirPath,file)
			templateImage = face_recognition.load_image_file(path)
			templateImage_encoding = face_recognition.face_encodings(templateImage)
			if templateImage_encoding == []:
				continue
			known_encodings = [templateImage_encoding[0],templateImage_encoding[0]]
			distance = face_recognition.face_distance(known_encodings,verifyImage_encoding[0])[0]
			confidence = 100 - distance * 100
			user = User.query.filter_by(path = path).first()
			if user:
				g.user = user
				face_token = g.user.generate_token()
				re.append({"cofidence":confidence,"face_token":face_token})

    if re == []:
    	return jsonify({"confidence":0})

	return jsonify({"results":re})	


if __name__ == '__main__':
	app.run(host = '0.0.0.0',port = 5002)	
 