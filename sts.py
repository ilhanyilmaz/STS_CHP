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
from bs4 import BeautifulSoup

URL = "http://sts.chp.org.tr"
CAPTCHA_URL = "http://sts.chp.org.tr/CreateCaptcha.aspx?New=1"
headers={
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", \
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36", \
	"Connection":"keep-alive", \
	"Content-Type":"application/x-www-form-urlencoded", \
	"DNT":"1", \
	"Host":"sts.chp.org.tr"
}

session = requests.Session()
session.headers.update(headers)

r1 = session.get(URL)


if not r1.reason == 'OK':
	print r1.reason
	exit()

sSetCookieStr = r1.headers["Set-Cookie"]
cookieStr =  sSetCookieStr[:sSetCookieStr.find(";")] + "; _ga=GA1.3.1703367742.1446899420; _gat=1"

session.headers.update({'Cookie':cookieStr})
session.headers.update({'Referer':URL+"/"})
session.headers.update({'Cache-Control':"max-age=0"})

soup = BeautifulSoup(r1.content)

sViewState = soup.find(id="__VIEWSTATE")['value']
sViewStateGenerator = ""
if not soup.find(id="__VIEWSTATEGENERATOR") == None:
	sViewStateGenerator = soup.find(id="__VIEWSTATEGENERATOR")['value']
sEventValidation = soup.find(id="__EVENTVALIDATION")['value']


##############################################################
r2 = session.get(CAPTCHA_URL)

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
##############################################################

code = raw_input("what's the input?\n")

session.headers.update({'Origin':URL})

dataDict = dict( \
	__EVENTTARGET="rdveriKaynagi$1", \
	__EVENTARGUMENT="", \
	__LASTFOCUS="", \
	__VIEWSTATE=sViewState, \
	__EVENTVALIDATION=sEventValidation, \
	rdveriKaynagi=2,\
	txtTCKN="",\
	txtCaptcha=""\
	)

r = session.post("http://sts.chp.org.tr/", data = dataDict)



dataDict = dict( \
	rdveriKaynagi=2, \
	dlIller= 1, \
	ddlIlceler= 650,  \
	ddlSandiklar= 2106007, \
	txtCaptcha= code, \
	btnSorgula="SORGULA", \
	__EVENTTARGET= "", \
	__EVENTARGUMENT= "", \
	__LASTFOCUS= "", \
	__VIEWSTATE= sViewState, \
	__VIEWSTATEGENERATOR= sViewStateGenerator, \
	__EVENTVALIDATION= sEventValidation \
	)


r = session.post("http://sts.chp.org.tr/", data = dataDict)
print session.headers
print r.status_code
print r.headers
#print r.content
r1.connection.close()
r2.connection.close()
r.connection.close()




#cv2.destroyAllWindows()


