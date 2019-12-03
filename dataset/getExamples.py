import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

EXAMPLES = 600
DEST_FOLDER = "/home/tavo/Escritorio/vaha captcha solver/dataset/examples/"
URL_CAPTCHA = "https://vahan.nic.in/nrservices/cap_img.jsp"

headers = {
	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0",
	"Accept": "image/webp,*/*", #"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Language": "es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3",
	"Accept-Encoding": "gzip, deflate, br",
	"Referer": "https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml",
	#"Content-Type": "application/x-www-form-urlencoded",
	# Content-Length: 32710
	"Connection": "keep-alive",
	"Host": "vahan.nic.in",
	# Cookie: JSESSIONID=DF542029C69BF1866876763FD33C717C.worker3; SERVERID_7082=nrservice_7084; SERVERID_7081=vahanapi_7081
	"Cache-Control" : "max-age=0"

}


with requests.Session() as s:
	i=0
	while True:
		try:
			imr = s.get(URL_CAPTCHA,headers = headers) #parte clave, obtener el captcha
			im = Image.open(BytesIO(imr.content))
			im.save(DEST_FOLDER+str(i)+".png", "PNG")
			print("Image "+str(i+1)+" of "+str(EXAMPLES))
			i+=1	
		except requests.exceptions.ConnectionError:
			print("Conection error")
		except requests.exceptions.Timeout:
			print("Timeout")

		if i==EXAMPLES:
			break