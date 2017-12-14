import face_recognition
import pickle
verifyImage = face_recognition.load_image_file("/Users/juntaoliu/Desktop/face/testImages/1.jpg")
verifyImage_encoding = face_recognition.face_encodings(verifyImage)[0]
print verifyImage_encoding
f = open("test.txt",'wb')
pickle.dump(verifyImage_encoding,f)
f.close()

f = open("test.txt",'rb')
d = pickle.load(f)
f.close()
print d
print d == verifyImage_encoding
