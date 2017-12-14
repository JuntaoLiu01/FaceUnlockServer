import requests

files = {'image': open('obama2.jpg', 'rb')}
user_info = {'API_KEY': 'pre_key'}
faceset_token = {"faceset_token":"eyJhbGciOiJIUzI1NiIsImV4cCI6MTUxNTgyMzE5MiwiaWF0IjoxNTEzMjMxMTkyfQ.eyJpZCI6M30.vRqz0aiXjObICu0jAa1O1tvdk20kK7zNBVqhkDvCkI0"}
face_token1 = {"face_token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTUxNTgyMzAyNCwiaWF0IjoxNTEzMjMxMDI0fQ.eyJpZCI6MX0.Z8lALu8YUYA9bDu5UaPk59yjvUIKhJorE2MyEsvWKfc"}
face_token2 = {"face_token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTUxNTgyMzExOCwiaWF0IjoxNTEzMjMxMTE4fQ.eyJpZCI6Mn0.J6xJlAcyasovI-VxKKO69AlSI4KTEMAUqsVOBYMdo-Q"}

add_face = {'API_KEY': 'pre_key',"face_token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTUxNTgyMzExOCwiaWF0IjoxNTEzMjMxMTE4fQ.eyJpZCI6Mn0.J6xJlAcyasovI-VxKKO69AlSI4KTEMAUqsVOBYMdo-Q",
				"faceset_token":"eyJhbGciOiJIUzI1NiIsImV4cCI6MTUxNTgyMzE5MiwiaWF0IjoxNTEzMjMxMTkyfQ.eyJpZCI6M30.vRqz0aiXjObICu0jAa1O1tvdk20kK7zNBVqhkDvCkI0"}

delete_face = {'API_KEY': 'pre_key',"face_token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTUxNTgyMTMzNSwiaWF0IjoxNTEzMjI5MzM1fQ.eyJpZCI6MTR9.Tt_PBOfyY6G65UlzQF3nA76yKkVHj78AuX584MW6MBw",
				"faceset_token":"eyJhbGciOiJIUzI1NiIsImV4cCI6MTUxNTgyMDk3NCwiaWF0IjoxNTEzMjI4OTc0fQ.eyJpZCI6MTN9.uqD41wXGmAyYnNoYf6qbmtJHGtmi9DAS704KqGC0DlY"}

search_face = {'API_KEY': 'pre_key',"faceset_token":"eyJhbGciOiJIUzI1NiIsImV4cCI6MTUxNTgyMzE5MiwiaWF0IjoxNTEzMjMxMTkyfQ.eyJpZCI6M30.vRqz0aiXjObICu0jAa1O1tvdk20kK7zNBVqhkDvCkI0"}

#detect_face
#r = requests.post("http://127.0.0.1:5000/detect", data=user_info, files=files)

#create_set
#r = requests.post("http://127.0.0.1:5000/create_set", data=user_info)

#add_face
#r = requests.post("http://127.0.0.1:5000/add_face", data=add_face)

#delete_face
#r = requests.post("http://127.0.0.1:5000/delete_face", data=delete_face)

#search_face
r = requests.post("http://127.0.0.1:5000/search_face", data=search_face, files=files)


print r.text