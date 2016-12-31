xsltproc --path "." --stringparam 'noentities' 'noentities' --stringparam 'autoinit' 'autoinit' --novalid ../etc/isaw-papers2awdl.xsl ../../isaw/isaw-papers/isaw-papers-3/isaw-papers-3.xhtml > index.xhtml 
cp ../../isaw/isaw-papers/isaw-papers.css .
