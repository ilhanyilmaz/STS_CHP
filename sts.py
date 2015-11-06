#import httplib
#h1 = httplib.HTTPConnection('sts.chp.org.tr:80')
#h1.request("GET", "/")
#r1 = h1.getresponse()
#if not r1.status == 200:
#	print r1.status, r1.reason
#	exit()

import requests
import cv2
import numpy as np
from PIL import Image

session = requests.Session()
r1 = session.get('http://sts.chp.org.tr')

if not r1.reason == 'OK':
	print r1.reason
	exit()

data1 = r1.content
tempPos = data1.find('__VIEWSTATE')
tempPos = tempPos + 37
str2 = data1[tempPos:]
tempPos = str2.find('\"')
sViewState = str2[:tempPos]
tempPos1 = str2.find('__VIEWSTATEGENERATOR') + 55
tempPos2 = str2.find('\"', tempPos1)
sViewStateGenerator = str2[tempPos1:tempPos2]
tempPos1 = str2.find('__EVENTVALIDATION') + 49
tempPos2 = str2.find('\"', tempPos1)
sEventValidation = str2[tempPos1:tempPos2]

r2 = session.get("http://sts.chp.org.tr/CreateCaptcha.aspx?New=1")

if not r2.reason == 'OK':
	print r2.reason
	exit()

data2 = r2.content
tempPos = data2.find('<!DOCTYPE html>')

f = open('test.gif', 'w')
f.write(data2)
f.close()

Image.open('test.gif').convert('RGB').save('test.jpg')

img = cv2.imread('test.jpg')

gray = img[:,:,2]
ret, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)


cv2.imshow('image', thresh)
cv2.waitKey(0)
cv2.destroyWindow('image')

code = raw_input("what's the input?\n")

postData = {
	"rdveriKaynagi":"2", \
	"dlIller": "1", \
	"ddlIlceler": "650",  \
	"ddlSandiklar": "2106007", \
	"txtCaptcha": code, \
	"btnSorgula": "SORGULA", \
	"__EVENTTARGET": "", \
	"__EVENTARGUMENT": "", \
	"__LASTFOCUS": "", \
	"__VIEWSTATE": sViewState, \
	"__VIEWSTATEGENERATOR": sViewStateGenerator, \
	"__EVENTVALIDATION": sEventValidation
	}

r = session.post("http://sts.chp.org.tr/", data = postData)

print r.status_code
#print r.headers

r1.connection.close()
r2.connection.close()
r.connection.close()




#cv2.destroyAllWindows()


