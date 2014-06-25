xsltproc --path "." --stringparam 'noentities' 'noentities' --stringparam 'autoinit' 'autoinit' --novalid ../etc/isaw-papers2awdl.xsl ../../isaw/isaw-papers/isaw-papers-5/isaw-papers-5.xhtml > index.xhtml 
cp ../../isaw/isaw-papers/isaw-papers.css .
