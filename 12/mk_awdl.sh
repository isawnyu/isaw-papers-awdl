cp ../../isaw/isaw-papers/isaw-papers-12/isaw-papers-12.xhtml .
cp ../../isaw/isaw-papers/isaw-papers-12/images/* images/
cp ../../isaw/isaw-papers/isaw-papers-12/isaw-publications.css .
xsltproc --path "." --stringparam 'noentities' 'noentities' --stringparam 'autoinit' 'autoinit' --novalid ../etc/isaw-papers2awdl.xsl ../../isaw/isaw-papers/isaw-papers-12/isaw-papers-12.xhtml | perl -pe 's/PUBLIC "" ""//'> index.xhtml 
