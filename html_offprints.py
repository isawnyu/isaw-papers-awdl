import base64
from bs4 import BeautifulSoup
import os
import shutil
import re
from wand.image import Image
from wand.display import display

def image64(images, path, soup, *path_dlib) :
	""" Encodes the images in base64 and replace the link to the images in the html by the encoded image
    
    :param images: list of images
    :type images: BeautifulSoup object
    :param path: path to the article in which we want to replace images 
    :type path: str
    :param soup: the whole article
    :type soup: BeautifulSoup object
    """
	i64 = []
	for i in range(0, len(images)):
		source = images[i]["src"]
		with Image(filename=str(path)+str(source)) as imageFile: 
			imageFile.transform('','1024x1024')
			if not os.path.isdir(str(j)+"/images"):
				os.makedirs(str(j)+"/images")
			imageFile.save(filename=str(j)+"/"+str(source))
		
		with open(str(j)+"/"+str(source), "rb") as image:
			print(image)
			im64 = base64.b64encode(image.read())
			i64.append(str(im64).replace("b'", "").replace("'",""))
		
		source = source.replace("images/", "").replace(".png", "").replace(".jpg", "").replace(".gif", "")
		if path_dlib : 
			images[i].wrap(soup.new_tag("a", href=path_dlib[0]+"#"+source))
		else : 
			images[i].wrap(soup.new_tag("a", href="http://dlib.nyu.edu/awdl/isaw/isaw-papers/"+str(j)+"/#"+source))

		images[i]["src"] = "data:image/png;base64,"+str(i64[i])
		if os.path.isdir(str(j)+"/images"):
			shutil.rmtree(str(j)+"/images")

def css(soup) :
	"""Adds the content of extern file publication.css to the html file of an article
   
    :param soup: the whole article
    :type soup: BeautifulSoup object
    """
	css_link = soup.find("link", {"rel" : re.compile("stylesheet*")})
	css_link.decompose()
	with open("isaw-papers/isaw-publications.css", "r") as css_file :
			css = css_file.read()
	css = css.replace("<http://isaw.nyu.edu/publications/isaw-papers>", "&lt;http://isaw.nyu.edu/publications/isaw-papers&gt;")
	soup.head.append(soup.new_tag("style"))
	soup.head.style.append(css)

def js_figures(soup, *path_dlib):
	"""Adds javascript element in the figure elements to help the citation of the figure
   
    :param soup: the whole article
    :type soup: BeautifulSoup object
    """
	figures = soup.find_all("figure", {"id": True})
	if figures :
		for figure in figures : 
			ids = figure["id"]
			figure["onmouseleave"] = "document.getElementById('"+ids+"anchor').style.display='none';document.getElementById('"+ids+"anchor_label').style.display='none';"
		
			figure["onmouseover"] = "document.getElementById('"+ids+"anchor').style.display='';document.getElementById('"+ids+"anchor_label').style.display='';" 
			if path_dlib : 
				link = soup.new_tag("a", id=ids+"anchor", style="color:#aaa;display:none", href=path_dlib[0]+"#"+ids)
			else : 
				link = soup.new_tag("a", id=ids+"anchor", style="color:#aaa;display:none", href="http://dlib.nyu.edu/awdl/isaw/isaw-papers/"+str(j)+"/#"+ids)
			link.append("⬈")
			span = soup.new_tag("span", id=ids+'anchor_label', style="color:#aaa;display:none;position:fixed;right:0;bottom:50%" )
			span.append("#"+ids)
			if figure.figcaption : 
				figure.figcaption.append(span)
				figure.figcaption.append(link)

def js_p(soup, *path_dlib) :	
	"""Adds javascript element in the paragraphs elements to help the citation of the paragraphs
   
    :param soup: the whole article
    :type soup: BeautifulSoup object
    """
	paragraphs = soup.find_all("p", {"id": True})
	for p in paragraphs :
		if not p.parent.name == "figcaption" and not p.img:
			ids = p["id"]
			p["onmouseleave"] = "document.getElementById('"+ids+"anchor').style.display='none';document.getElementById('"+ids+"anchor_label').style.display='none';"
			p["onmouseover"] = "document.getElementById('"+ids+"anchor').style.display='';document.getElementById('"+ids+"anchor_label').style.display='';" 
			if path_dlib :
				link = soup.new_tag("a", id=ids+"anchor", style="color:#aaa;display:none", href=path_dlib[0]+"#"+ids )
			else : 
				link = soup.new_tag("a", id=ids+"anchor", style="color:#aaa;display:none", href="http://dlib.nyu.edu/awdl/isaw/isaw-papers/"+str(j)+"/#"+ids )

			link["class"] = "id_link"
			link.append("⬈")
			p.append(link)
			span = soup.new_tag("span", id=ids+'anchor_label', style="color:#aaa;display:none;position:fixed;right:0;bottom:50%" )
			span["class"] = "id_label"
			span.append("#"+ids)
			p.append(span)

def header(head, soup, download_link):
	"""Adds the content of the external file head.xml in the html file of an article and includes link to download the file
   
    :param head: content of head.xml
    :type head: str
    :param soup: the whole article
    :type soup: BeautifulSoup object
    """
	div_head = ""
	
	download_message = head.new_tag("p", style="text-align:center;margin-top:1em")
	
	download_link.append("single file")
	download_message.append("This article can be downloaded as a ")
	download_message.append(download_link)
	div_head = head.div
	div_head.append(download_message)
	soup.header.insert(0, div_head)


def video(soup):
	"""Replaces relative links to the videos by absolute links 

    :param soup: the whole article
    :type soup: BeautifulSoup object
    """
	if soup.video:
		mp4s = soup.find_all("source", {"type" : "video/mp4"})
		for mp4 in mp4s :
			relative = mp4["src"]
			absolute = "http://dlib.nyu.edu/awdl/isaw/isaw-papers/"+str(j)+"/"+relative
			mp4["src"] = absolute 
		webms = soup.find_all("source", {"type" : "video/webm"})
		for webm in webms :
			relative = webm["src"]
			absolute = "http://dlib.nyu.edu/awdl/isaw/isaw-papers/"+str(j)+"/"+relative
			webm["src"] = absolute 

# Creating a global index file for the github siteweb
with open("index.md", "w") as download_page:
	download_page.write("""# ISAW Papers Articles standalone XHTML file


The journal is accessible online here : <a href="http://isaw.nyu.edu/publications/isaw-papers">http://isaw.nyu.edu/publications/isaw-papers</a>.

Unless otherwise noted all content is distributed under a Creative Commons Atribution license. See <a href="http://creativecommons.org/licenses/by/4.0/">http://creativecommons.org/licenses/by/4.0/</a>.

Feedback can be left by open an issue on the <a href="https://github.com/fmezard/isaw-papers-awdl/">GitHub repository</a> that hosts this content.

""")

for j in range(1, 14) :
	# Opening every articles and creating a BeautifulSoup object with all the modifications
	with open("isaw-papers/isaw-papers-"+str(j)+"/isaw-papers-"+str(j)+".xhtml", "r") as article :
		soup = BeautifulSoup(article,"html.parser")
	images = soup.find_all("img", {"src" : re.compile("images/*")}) 
	path = "isaw-papers/isaw-papers-"+str(j)+"/"
	
	image64(images, path, soup)
	css(soup)
	js_p(soup)
	js_figures(soup)
	video(soup)

	with open(str(j)+"/head.xml", "r") as head:
		head = BeautifulSoup(head, "html.parser")
		download_link = head.new_tag("a", href="http://dlib.nyu.edu/awdl/isaw/isaw-papers/"+str(j)+"/isaw-papers-"+str(j)+"-offprint.xhtml")
		download_link["download"] = "isaw-papers-"+str(j)
		header(head, soup, download_link)

	# Collection of articles ISAW Papers 7 (other numbers can be added if future articles are collections)
	if j == 7 : 
		for element in os.listdir('isaw-papers/isaw-papers-'+str(j)):
			if os.path.isdir('isaw-papers/isaw-papers-'+str(j)+ '/'+str(element)):
				for el in os.listdir('isaw-papers/isaw-papers-'+ str(j)+ '/'+ str(element)):
					
					if re.match("isaw-papers-"+str(j)+"-*", str(el)):
						with open ('isaw-papers/isaw-papers-'+str(j)+'/'+ str(element) + '/'+ str(el), "r") as article : 
							soup_7 = BeautifulSoup(article, "html.parser")
						dlib_path = "http://dlib.nyu.edu/awdl/isaw/isaw-papers/"+str(j)+"/"+str(element)+"/"

						if soup_7.img :
							images = soup_7.find_all("img") 			
							path = "isaw-papers/isaw-papers-"+str(j)+"/"+str(element) + "/"
							image64(images, path, soup, dlib_path)
						el = el.replace('.xhtml', '')
						css(soup_7)
						js_figures(soup_7, dlib_path)
						js_p(soup_7, dlib_path)
						video(soup_7)
						with open(str(j)+'/'+ str(element) + "/head.xml", "r") as head:
							head = BeautifulSoup(head, "html.parser")
							download_link = head.new_tag("a", href="http://dlib.nyu.edu/awdl/isaw/isaw-papers/"+str(j)+"/"+str(element)+"/"+str(el)+"-offprint.xhtml")
							download_link["download"] = el 
							header(head, soup_7, download_link)

						paragraphs_footer = soup_7.footer.find_all("p")

						for p in paragraphs_footer : 
							p["style"] = "margin-top:1em;text-align:center;color:gray"
							links = p.find_all("a")
							for link in links :
								link["style"] = "color:gray"

						if not os.path.exists(str(j)+'/'+ str(element)):
							os.makedirs(str(j)+'/'+ str(element))
						print(el)
						with open (str(j)+'/'+ str(element) + '/'+ str(el)+"-offprint.xhtml", "w") as article : 
							article.write(str(soup_7))
						with open (str(j)+'/'+ str(element) + "/index.xhtml", "w") as article : 
							article.write(str(soup_7))

	# Creating the standalone xhtml files from the BeautifulSoup object
	with open(str(j)+"/isaw-papers-"+str(j)+"-offprint.xhtml", "w") as article :
		article.write(str(soup))

	with open (str(j)+"/index.xhtml", "w") as article :
		article.write(str(soup))

	# adding the link to the article in the general index file
	with open("index.md", "a") as download_page:
		download_page.write("ISAW Papers "+str(j)+"  \n---\n<a href='"+str(j)+"/isaw-papers-"+str(j)+"-offprint.xhtml' download>Click to download</a>  \n<a href='"+str(j)+"/isaw-papers-"+str(j)+"-offprint.xhtml'>Click to see in browser</a>\n\n")
