import base64
from bs4 import BeautifulSoup    
import os
import re

i64 = []

for filename in os.listdir("10/images_small"):
    with open("10/images_small/"+filename, "rb") as imageFile:
        im64 = base64.b64encode(imageFile.read())
        i64.append(str(im64).replace("b'", "").replace("'",""))


with open("10/index.xhtml", "r") as article :
	soup = BeautifulSoup(article, "lxml")
images = soup.find_all("img", {"src" : re.compile("images/*")}) 

with open("10/isaw-papers.css", "r") as css_file :
	css = css_file.read()

soup.head.append(soup.new_tag("style"))
soup.head.style.append(css)


for i in range(0, len(images)):
	source = images[i]["src"]
	source = source.replace("images/", "").replace(".png", "")
	images[i].wrap(soup.new_tag("a", href="http://dlib.nyu.edu/awdl/isaw/isaw-papers/10/#"+source))
	images[i]["src"] = "data:image/png;base64,"+str(i64[i])


with open("10/index_image64.xhtml", "w") as article :
	article.write(str(soup))
