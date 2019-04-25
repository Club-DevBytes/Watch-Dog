# virtualenv -p python3 envname
# cd faceEnv/bin/
# source activate
# source deactivate


import urllib.request, urllib.parse, urllib.error, http.client, base64, json
import requests

group_id = 'students' # name of personGroup
personList = [] 
KEY = ''

# faceID = ['c78ff3cb-e592-458f-8612-99eded91d3e4']


from twilio.rest import Client
auth_token = '' # twilio authorization token
account_sid = ''


# import boto3
# session = boto3.Session(
# #     aws_access_key_id=ACCESS_KEY,
# #     aws_secret_access_key=SECRET_KEY,
# #     aws_session_token=SESSION_TOKEN
# )

from picamera import PiCamera
#*****Camera Setup*****#
camera = PiCamera() # initiate camera
camera.rotation = 180 # Used to correct orientation of camera
BaseDirectory = '/home/pi/Desktop/azure-faceApi/captured/' # directory where picamera photos are stored
import time 
import datetime
import os

import glob #to get latest added file 

faceIdList = []

import sys

bucketName = 'faceapiazure' # aws s3 bucket name


import cloudinary
import cloudinary.uploader

cloudinary.config( 
  cloud_name = "", 
  api_key = "", 
  api_secret = "" 
)

import pyrebase
config = {
  "apiKey": "",
  "authDomain": "fir-trial-7eebb.firebaseapp.com",
  "databaseURL": "https://fir-trial-7eebb.firebaseio.com",
  "storageBucket": "fir-trial-7eebb.appspot.com"
}
import subprocess 
firebase = pyrebase.initialize_app(config)
db = firebase.database()


def identify(ids):
        headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': KEY}
        params = urllib.parse.urlencode({'personGroupId': group_id})
        body = "{'personGroupId':'students', 'faceIds':"+str(ids)+"}"
        conn = http.client.HTTPSConnection('centralindia.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/identify?%s" % params, body, headers)
        response = conn.getresponse()

        data = json.loads(response.read().decode('utf-8')) # turns response into index-able dictionary

        for resp in data:
            candidates = resp['candidates']
            for candidate in candidates: # for each candidate in the response
                # confidence = candidate['confidence'] # retrieve confidence
                personId = str(candidate['personId']) # and personId
                personList.append(personId)
        conn.close()
        print(personList)



# takes in person_id and retrieves known person's name with azure GET request
def getNameAndPhoneNo(person_Id):
    headers = {'Ocp-Apim-Subscription-Key': KEY}
    params = urllib.parse.urlencode({'personGroupId': group_id, 'personId': person_Id})

    conn = http.client.HTTPSConnection('centralindia.api.cognitive.microsoft.com')
    conn.request("GET", "/face/v1.0/persongroups/{"+group_id+"}/persons/"+person_Id+"?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = json.loads(response.read().decode('utf-8'))
    name = data['name']

    userData = data['userData']
    
    UserDataRead = json.loads(userData)

    phoneNo = UserDataRead['phoneNo']    

    conn.close()
    print(name)
    print(userData)
    print(phoneNo)

    return name, phoneNo


# uses twilio rest api to send mms message, takes in message as body of text, and url of image
def twilio(name,phoneNo, imageLink):
    client = Client(account_sid, auth_token)
    msg = name+" is present"
    message = client.messages.create(to='+123456789', from_='+1155454545', body = msg, media_url=imageLink)
    
    message1 = client.messages.create(to= phoneNo , from_='+156565656', body = msg, media_url=imageLink)

    print((message.sid))
    print((message1.sid))

def twilio_Intruder(imageLink):
    client = Client(account_sid, auth_token)
    msg = "Intruder Detected at location pi cam 1"
    message = client.messages.create(to='+5454545454', from_='+12018775310', body = msg, media_url=imageLink)    
    print((message.sid))

def twilio_Detained(name, imageLink):
    client = Client(account_sid, auth_token)
    msg = name+": is Detained and is located at pi cam 1"
    message = client.messages.create(to='+917984677074 ', from_='+12018775310', body = msg, media_url=imageLink)

    print((message.sid))

def twilio_Suspicious(imageLink):
    client = Client(account_sid, auth_token)
    msg = "Suspicious activity detected at pi cam 1"
    message = client.messages.create(to='+917984677074 ', from_='+12018775310', body = msg, media_url=imageLink)    
    print((message.sid))

def cloudinaryUpload(imgPath):
        resp =  cloudinary.uploader.upload(imgPath)
        url = resp["secure_url"]
        print(url)
        return url
# # uses aws s3 to upload photos
# def uploadPhoto(fName):
#     s3 = session.resource('s3')a
#     data = open(fName, 'rb')
#     s3.Bucket(bucketName).put_object(Key=fName, Body=data, ContentType = 'image/jpeg')

#     # makes uploaded image link public
#     object_acl = s3.ObjectAcl(bucketName, fName)
#     response = object_acl.put(ACL='public-read')

#     link = 'https://s3.amazonaws.com/'+bucketName+'/'+fName
#     return link


def camCapture():
        directory = BaseDirectory
        date = datetime.datetime.now().strftime('%m_%d_%Y_%M_%S_') # change file name for every photo
        camera.capture(directory + date +'.jpg')
        print((directory+" pic saved"))


def latestFile():

        list_of_files = glob.glob(BaseDirectory + '*') # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        print (latest_file)
        return latest_file

camCapture()





imgUrl = cloudinaryUpload(latestFile())
time_set = datetime.datetime.now().strftime ("%H:%M:%S")
date = datetime.datetime.now().strftime ("%Y-%m-%d")


def ultra():
    os.system("python /home/pi/Desktop/ultra.py")



def detectFace(imgPath):
    headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': KEY}
    body = open(imgPath ,'rb')
    params = urllib.parse.urlencode({'returnFaceId': 'true'})
    conn = http.client.HTTPSConnection('centralindia.api.cognitive.microsoft.com')# this should be taken from your endpoint
    conn.request("POST", '/face/v1.0/detect?%s' % params, body, headers) # this is the specific endpoint
    response = conn.getresponse()
    photo_data = json.loads(response.read().decode('utf-8'))
    print(photo_data)
    
    if not photo_data: # if post is empty (meaning no face found)
        print('Suspicious activity detected!!')
        twilio_Suspicious(imgUrl)
        db.child("Suspicious").child(date).child(time_set).child("img").set(imgUrl) 
        os.system("python /home/pi/Desktop/ultra.py")
    # elif name == "Jainal Gosaliya": 
    #     print('Expelled Student Detected')
    #     twilio_Detained(name, imgUrl)
    #     db.child("Detained").child(date).child(personList[0]).child("name").set(name)
        # os.system("python /home/pi/Desktop/ultra.py")
        #ultra()
    else: # if face is found
        for face in photo_data: # for the faces identified in each photo
            faceIdList.append(str(face['faceId'])) # get faceId for use in identify   
         # {u'secure_url': u'https://res.cloudinary.com/dvey2m05b/image/upload/v1547531078/zb23mvnwr6azrgthtcbj.jpg', u'public_id': u'zb23mvnwr6azrgthtcbj', u'format': u'jpg', u'url': u'http://res.cloudinary.com/dvey2m05b/image/upload/v1547531078/zb23mvnwr6azrgthtcbj.jpg', u'placeholder': False, u'created_at': u'2019-01-15T05:44:38Z', u'tags': [], u'bytes': 1161365, u'height': 1080, u'width': 1920, u'version': 1547531078, u'etag': u'45f5741be538aa7e45445d338904affc', u'original_filename': u'01_15_2019_14_18_', u'signature': u'7707df8fca4d399e63f12033fcaa33f666c08006', u'type': u'upload', u'resource_type': u'image'}

 

detectFace(latestFile())
identify(faceIdList)
print(faceIdList)

if personList == []: # if post is empty (meaning no face found)
                print('Warning Unauthorized person Detected')
                print("Unknown Face Detected!!")
                db.child("Unauthorized").child(date).child(time_set).child("img").set(imgUrl)

                twilio_Intruder(imgUrl)
                os.system("python /home/pi/Desktop/ultra.py")
name, phoneNo = getNameAndPhoneNo(personList[0])


# time = datetime.datetime.now().strftime ("%H:%M:%S")
db.child("attendence").child(date).child(personList[0]).child("name").set(name)
db.child("attendence").child(date).child(personList[0]).child("img").set(imgUrl)


twilio(name,phoneNo,imgUrl)

os.system("python /home/pi/Desktop/ultra.py")
# sudo -H pip2.7 install
