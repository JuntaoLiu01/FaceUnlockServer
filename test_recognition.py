import face_recognition

# Often instead of just checking if two faces match or not (True or False), it's helpful to see how similar they are.
# You can do that by using the face_distance function.

# The model was trained in a way that faces with a distance of 0.6 or less should be a match. But if you want to
# be more strict, you can look for a smaller face distance. For example, using a 0.55 cutoff would reduce false
# positive matches at the risk of more false negatives.

# Note: This isn't exactly the same as a "percent match". The scale isn't linear. But you can assume that images with a
# smaller distance are more similar to each other than ones with a larger distance.

# Load some images to compare against
known_obama_image = face_recognition.load_image_file("obama.jpg")
known_biden_image = face_recognition.load_image_file("biden.jpg")
known_1_image     = face_recognition.load_image_file("1.jpg")

# Get the face encodings for the known images
obama_face_encoding = face_recognition.face_encodings(known_obama_image)[0]
biden_face_encoding = face_recognition.face_encodings(known_biden_image)[0]
_1_face_encoding    = face_recognition.face_encodings(known_1_image)[0]

known_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    _1_face_encoding
]

# Load a test image and get encondings for it
image_to_test = face_recognition.load_image_file("obama2.jpg")
image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]

# See how far apart the test image is from the known faces
face_distances = face_recognition.face_distance(known_encodings, image_to_test_encoding)
print face_distances[0]