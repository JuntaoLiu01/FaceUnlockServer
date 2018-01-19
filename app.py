#-*- coding=utf-8 -*-
import os,shutil
import face_recognition
from utils.func import *
from config.const import *
from flask import Flask,request,g,jsonify
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


app = Flask(__name__)
app.config['SECRET_KEY']  = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['IMAGE_PATH'] = os.path.join(app.root_path,app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = DB_TABLE
	id  = db.Column(db.Integer,primary_key = True)
	path = db.Column(db.String(MAX_PATH_LENGTH))

	def generate_token(self, expiration = TOKEN_LIFE):
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
def detect():
    key = request.form['api_key']
    if not key == API_KEY:
    	return jsonify({"faces":[]})

    image = request.files['image_file']
    image = face_recognition.load_image_file(image)
    #if not file or not allowed_file(file.filename):
    	#return None

    l = generate_encodings(image)
    if l == []:
    	return jsonify({"faces":[]})

    fileName = generate_file_name() + ".txt"
    filePath = os.path.join(app.config['IMAGE_PATH'],fileName)
    save_encodings(filePath,l)
    
    user = User(path = fileName)
    db.session.add(user)
    db.session.commit()

    token = ""
    result = User.query.filter_by(path = fileName).first()
    if result:
    	g.user = result
    	token = g.user.generate_token()
    
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
    		"face_rectangle": face_retangle,
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
		return jsonify({"faceset_token" : ""})

	dirName = generate_file_name()
	dirPath = os.path.join(app.config['IMAGE_PATH'],dirName)

	if not os.path.exists(dirPath):
		os.mkdir(dirPath)

	user = User(path = dirName)
	db.session.add(user)
	db.session.commit()

	result = User.query.filter_by(path = dirName).first()
	g.user = result
	token = g.user.generate_token()

	return jsonify({"faceset_token" : token})

@app.route('/addface',methods = ['POST'])
def add_face():
	key = request.form["api_key"]
	if not key == API_KEY:
		return jsonify({"face_added":0})

	face_token  = request.form["face_token"]
	faceset_token = request.form["faceset_token"]

	face_user = User.verify_token(face_token)
	if not face_user:
		return jsonify({"face_added":0})

	faceset_user = User.verify_token(faceset_token)
	if not faceset_user:
		return jsonify({"face_added":0})

	fileName = face_user.path
	oldPath = os.path.join(app.config['IMAGE_PATH'],fileName)
	newPath = os.path.join(app.config['IMAGE_PATH'],faceset_user.path,fileName)
	shutil.move(oldPath,newPath)

	face_user.path = os.path.join(faceset_user.path,fileName)
	db.session.add(face_user)
	db.session.commit()

	return jsonify({"face_added":1})


@app.route('/removeface',methods = ['POST'])
def delete_face():
	key = request.form['api_key']
	if not key == API_KEY:
		return jsonify({"face_removed":0})

	face_token  = request.form["face_token"]
	#faceset_token = request.form["faceset_token"]

	face_user = User.verify_token(face_token)
	if not face_user:
		return jsonify({"face_removed":0})

	fileName = face_user.path
	path  = os.path.join(app.config['IMAGE_PATH'],fileName)
	os.remove(path)

	db.session.delete(face_user)
	db.session.commit()

	return jsonify({"face_removed":1})


@app.route('/search',methods = ['POST'])
def search_face():
	key = request.form['api_key']
	if not key == API_KEY:
		return jsonify({"results":[]})
    
	faceset_token = request.form["faceset_token"]
	faceset_user = User.verify_token(faceset_token)
	if not faceset_token:
		return jsonify({"results":[]})

	image = request.files["image_file"]
	#if not image or not allowed_file(image.filename):
		#return None

	verifyImage = face_recognition.load_image_file(image)
	verifyImage_encoding =  generate_encodings(verifyImage)
	if verifyImage_encoding == []:
		return jsonify({"results":[]})

	re  = []
	if not faceset_user:
		return jsonify({"results":[]})
	dirPath = os.path.join(app.config['IMAGE_PATH'],faceset_user.path)
	files = os.listdir(dirPath)
	for file in files:
		if not os.path.isdir(file):
			path = os.path.join(dirPath,file)
			templateImage_encoding = get_encodings(path)
			known_encodings = [templateImage_encoding,templateImage_encoding]
			distance = face_recognition.face_distance(known_encodings,verifyImage_encoding)[0]
			confidence = 100 - distance * 100
			filePath = os.path.join(faceset_user.path,file)
			user = User.query.filter_by(path = filePath).first()
			if user:
				g.user = user
				face_token = g.user.generate_token()
				re.append({"confidence":confidence,"face_token":face_token})

	return jsonify({"results":re})	


if __name__ == '__main__':
	app.run(host = LISTEN,port = PORT)	
 