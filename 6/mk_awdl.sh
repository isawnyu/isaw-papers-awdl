xsltproc --path "." --stringparam 'noentities' 'noentities' --stringparam 'autoinit' 'autoinit' --novalid ../etc/isaw-papers2awdl.xsl ../../isaw/isaw-papers/isaw-papers-6/isaw-papers-6.xhtml | perl -pe 's/PUBLIC "" ""//'> index.xhtml 
cp ../../isaw/isaw-papers/isaw-papers.css .
