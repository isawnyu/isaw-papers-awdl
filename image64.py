import base64
from bs4 import BeautifulSoup    
import os
import re

i64 = []

for filename in os.listdir("10/images"):
    with open("10/images/"+filename, "rb") as imageFile:
        im64 = base64.b64encode(imageFile.read())
        i64.append(str(im64).replace("b'", "").replace("'",""))


with open("10/index.xhtml", "r") as article :
	soup = BeautifulSoup(article, "lxml")
images = soup.find_all("img", {"src" : re.compile("images/*")}) 
for i in range(0, len(images)):
	images[i]["src"] = "data:image/png;base64,"+str(i64[i])

with open("10/index_image64.xhtml", "w") as article :
	article.write(str(soup))
