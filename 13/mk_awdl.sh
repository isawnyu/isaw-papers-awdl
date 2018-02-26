cp ../../isaw/isaw-papers/isaw-papers-13/isaw-papers-13.xhtml .
cp ../../isaw/isaw-papers/isaw-papers-13/images/* images/
cp ../../isaw/isaw-papers/isaw-papers-13/isaw-publications.css .
cp ../../isaw/isaw-papers/isaw-papers-13/isaw-papers-13-data* .
xsltproc --path "." --stringparam 'noentities' 'noentities' --stringparam 'autoinit' 'autoinit' --novalid ../etc/isaw-papers2awdl.xsl ../../isaw/isaw-papers/isaw-papers-13/isaw-papers-13.xhtml | perl -pe 's/PUBLIC "" ""//'> index.xhtml 
