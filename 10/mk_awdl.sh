cp ../../isaw/isaw-papers/isaw-papers-10/images/* images/
cp ../../isaw/isaw-papers/isaw-papers-10/isaw-papers.css .
xsltproc --path "." --stringparam 'noentities' 'noentities' --stringparam 'autoinit' 'autoinit' --novalid ../etc/isaw-papers2awdl.xsl ../../isaw/isaw-papers/isaw-papers-10/isaw-papers-10.xhtml | perl -pe 's/PUBLIC "" ""//'> index.xhtml 
