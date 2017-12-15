import pickle
import time,hashlib
import face_recognition

def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_file_name():
	ticks = time.time()
	return hashlib.md5(str(ticks)).hexdigest()

def generate_encodings(image):
	encodings = face_recognition.face_encodings(image)
	if encodings == []:
		return []
	return encodings[0]

def save_encodings(filePath,encodings):
	f = open(filePath,'wb')
	pickle.dump(encodings,f)
	f.close()

def get_encodings(filePath):
	f = open(filePath,'rb')
	encodings = pickle.load(f)
	f.close()
	return encodings