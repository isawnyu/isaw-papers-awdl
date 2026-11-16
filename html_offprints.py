import argparse
import base64
import hashlib
from bs4 import BeautifulSoup
import os
import shutil
import re
from wand.image import Image
from wand.display import display
import textwrap

# ISAW PAPERS DIR

ISAW_PAPERS_PREFIX = "../"

def image_key(source):
    """Fragment id used to link an image back to the article: its src without
    "images/" and without its extension (e.g. "images/figure01.png" -> "figure01")."""
    return source.replace("images/", "").replace(".png", "").replace(".jpg", "").replace(".gif", "")

def mime_type(data):
    """MIME type of image data, read from the file signature in its first bytes."""
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    raise ValueError("unrecognised image data")

def load_embedded_images(article_dir):
    """Images embedded in this article's previous output (article_dir/index.xhtml),
    keyed by image_key. Each entry holds the base64 text exactly as stored and the
    data-source-sha256 recorded when it was encoded (None for older outputs).

    :param article_dir: output directory of the article, e.g. "29-2"
    :type article_dir: str
    """
    previous = os.path.join(article_dir, "index.xhtml")
    found = {}
    if not os.path.exists(previous):
        return found
    with open(previous, "r") as f:
        old = BeautifulSoup(f, "html.parser")
    for img in old.find_all("img", src=re.compile(r"^data:image/[a-z]+;base64,")):
        link = img.parent
        if link is None or link.name != "a" or "#" not in link.get("href", ""):
            continue
        key = link["href"].rsplit("#", 1)[1]
        found.setdefault(key, {"b64": img["src"].split(",", 1)[1],
                               "sha256": img.get("data-source-sha256")})
    return found

def image64(images, path, soup, *path_dlib, previous=None, fresh=False) :
    """ Embeds the images in the html as base64 data and links each one to its place in the article.

    An image already embedded in the previous output is reused unchanged, so that
    regenerating an article does not re-encode its images. It is encoded from its
    source file instead when:
      - fresh is True (--fresh-images);
      - the previous output has no image for it (a new image, or no previous output);
      - the previous output recorded a data-source-sha256 that no longer matches the source file.
    Encoded images carry data-source-sha256 (the hash of the source file they were
    made from), so later runs can tell when a source image has changed. Images reused
    from outputs made before this attribute existed are reported as unverified and
    get no hash, since which source produced them is not known.

    :param images: list of images
    :type images: BeautifulSoup object
    :param path: path to the article in which we want to replace images
    :type path: str
    :param soup: the whole article
    :type soup: BeautifulSoup object
    :param previous: images embedded in the previous output, from load_embedded_images()
    :type previous: dict
    :param fresh: re-encode every image from its source file
    :type fresh: bool
    """
    previous = previous or {}
    counts = {}
    for img in images:
        source = img["src"]
        filename = str(ISAW_PAPERS_PREFIX + path) + str(source)
        with open(filename, "rb") as f:
            sha256 = hashlib.sha256(f.read()).hexdigest()
        key = image_key(source)
        old = previous.get(key)

        if fresh:
            outcome = "encoded (--fresh-images)"
        elif old is None:
            outcome = "encoded (not in previous output)"
        elif old["sha256"] is not None and old["sha256"] != sha256:
            outcome = "encoded (source changed)"
        elif old["sha256"] is not None:
            outcome = "reused (verified)"
        else:
            outcome = "reused (unverified)"
        counts[outcome] = counts.get(outcome, 0) + 1

        if outcome.startswith("reused"):
            b64 = old["b64"]
            head = base64.b64decode("".join(b64.split())[:16])
        else:
            with Image(filename=filename) as imageFile:
                imageFile.transform('','1024x1024')
                imageFile.format = 'jpeg'
                imageFile.compression_quality = 90
                imageFile.strip()
                data = imageFile.make_blob()
            flat = base64.b64encode(data).decode("ascii")
            wrap_n = 80
            b64 = '\n'.join(flat[k:k+wrap_n] for k in range(0, len(flat), wrap_n))
            head = data[:16]

        if path_dlib :
            img.wrap(soup.new_tag("a", href=path_dlib[0]+"#"+key))
        else :
            img.wrap(soup.new_tag("a", href="https://awdl.dlib.nyu.edu/isaw/isaw-papers/"+str(j)+"/#"+key))

        img["src"] = "data:" + mime_type(head) + ";base64," + b64
        if outcome == "reused (unverified)":
            if "data-source-sha256" in img.attrs:
                del img["data-source-sha256"]
        else:
            img["data-source-sha256"] = sha256

    summary = ", ".join("%d %s" % (n, outcome) for outcome, n in sorted(counts.items()))
    print("%s: %d images%s" % (j, len(images), ": " + summary if summary else ""))

def css(path, soup) :
    """Adds the content of extern file publication.css to the html file of an article

    :param soup: the whole article
    :type soup: BeautifulSoup object
    """
    css_link = soup.find("link", {"rel" : re.compile("stylesheet*")})
    css_link.decompose()
    with open(ISAW_PAPERS_PREFIX + path + "isaw-publications.css", "r") as css_file :
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
                link = soup.new_tag("a", id=ids+"anchor", style="color:#aaa;display:none", href="https://awdl.dlib.nyu.edu/isaw/isaw-papers/"+str(j)+"/#"+ids)
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
                link = soup.new_tag("a", id=ids+"anchor", style="color:#aaa;display:none", href="https://awdl.dlib.nyu.edu/isaw/isaw-papers/"+str(j)+"/#"+ids )

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
    download_message.append("Download as a ")
    download_message.append(download_link)
    download_message.append(".")
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
            absolute = "https://awdl.dlib.nyu.edu/isaw/isaw-papers/"+str(j)+"/"+relative
            mp4["src"] = absolute
        webms = soup.find_all("source", {"type" : "video/webm"})
        for webm in webms :
            relative = webm["src"]
            absolute = "https://awdl.dlib.nyu.edu/isaw/isaw-papers/"+str(j)+"/"+relative
            webm["src"] = absolute

# Creating a global index file for the github siteweb
#with open("index.md", "w") as download_page:
#    download_page.write(""" ISAW Papers Articles standalone XHTML file


#The journal is accessible online here : <a href="http://isaw.nyu.edu/publications/isaw-papers">http://isaw.nyu.edu/publications/isaw-papers</a>.

#Unless otherwise noted all content is distributed under a Creative Commons Atribution license. See <a href="http://creativecommons.org/licenses/by/4.0/">http://creativecommons.org/licenses/by/4.0/</a>.

#Feedback can be left by open an issue on the <a href="https://github.com/fmezard/isaw-papers-awdl/">GitHub repository</a> that hosts this content.

#""")

# build dir array

papers_list = ['18','18-1','18-2','18-3','18-4','18-5','18-6','18-7','18-8','18-9','18-10','18-11','19']
papers_list = ['20','20-1','20-2','20-3','20-4','20-5','20-6','20-7','20-8','20-9','20-10','20-11','20-12','20-13']

papers_list = ['29-6']

parser = argparse.ArgumentParser()
parser.add_argument("--articles", required=True,
                    help="article ids to render, comma- or space-separated, "
                         "e.g. --articles 29-6 or --articles '29-5,29-6'")
parser.add_argument("--fresh-images", action="store_true",
                    help="re-encode every image from its source file instead of "
                         "reusing the images embedded in the previous output")
args = parser.parse_args()
if args.articles:
    papers_list = args.articles.replace(",", " ").split()


for j in papers_list :
    # Opening every article and creating a BeautifulSoup object with all the modifications
    with open(ISAW_PAPERS_PREFIX + "isaw-papers/isaw-papers-"+str(j)+"/isaw-papers-"+str(j)+".xhtml", "r") as article :
        soup = BeautifulSoup(article,"html.parser")
    images = soup.find_all("img", {"src" : re.compile("images/*")})
    path = "isaw-papers/isaw-papers-"+str(j)+"/"
    
    image64(images, path, soup, previous=load_embedded_images(str(j)), fresh=args.fresh_images)
    css(path, soup)
    js_p(soup)
    js_figures(soup)
    video(soup)

    with open(str(j)+"/head.xml", "r") as head:
        head = BeautifulSoup(head, "html.parser")
        download_link = head.new_tag("a", href="https://awdl.dlib.nyu.edu/isaw/isaw-papers/"+str(j)+"/isaw-papers-"+str(j)+"-offprint.xhtml")
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
#    with open("index.md", "a") as download_page:
#        download_page.write("ISAW Papers "+str(j)+"  \n---\n<a href='"+str(j)+"/isaw-papers-"+str(j)+"-offprint.xhtml' download>Click to download</a>  \n<a href='"+str(j)+"/isaw-papers-"+str(j)+"-offprint.xhtml'>Click to see in browser</a>\n\n")
