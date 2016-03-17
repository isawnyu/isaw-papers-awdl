cp ../../isaw/isaw-papers/isaw-papers-11/images/* images/
cp ../../isaw/isaw-papers/isaw-papers-11/isaw-publications.css .
xsltproc --path "." --stringparam 'noentities' 'noentities' --stringparam 'autoinit' 'autoinit' --novalid ../etc/isaw-papers2awdl.xsl ../../isaw/isaw-papers/isaw-papers-11/isaw-papers-11.xhtml | perl -pe 's/PUBLIC "" ""//'> index.xhtml 
