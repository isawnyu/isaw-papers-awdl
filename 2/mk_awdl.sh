xsltproc --path "." --stringparam 'autoinit' 'autoinit' --novalid ../etc/isaw-papers2awdl.xsl ../../isaw/isaw-papers/isaw-papers-2/isaw-papers-2.html > index.xhtml 
cp ../../isaw/isaw-papers/isaw-papers.css .
