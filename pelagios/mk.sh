cat head.txt > isaw-papers-pelagios.rdf
 xsltproc --stringparam 'ipnum' '2' ip2pelagios.xsl ../../isaw/isaw-papers/isaw-papers-2/isaw-papers-2.html >> isaw-papers-pelagios.rdf
 xsltproc --stringparam 'ipnum' '3' ip2pelagios.xsl ../../isaw/isaw-papers/isaw-papers-3/isaw-papers-3.html >> isaw-papers-pelagios.rdf
cat foot.txt >> isaw-papers-pelagios.rdf

