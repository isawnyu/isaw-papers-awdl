xsltproc --path "." --stringparam 'noentities' 'noentities' --novalid --stringparam 'autoinit' 'autoinit' ../etc/isaw-papers2awdl.xsl ../../isaw/isaw-papers/isaw-papers-1/isaw-papers-1.html  > index.xhtml
cp ../../isaw/isaw-papers/isaw-papers.css .
