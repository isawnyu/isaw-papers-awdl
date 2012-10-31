<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:h="http://www.w3.org/1999/xhtml"
 xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
 xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
 xmlns:oac="http://www.openannotation.org/ns/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 >
 <xsl:output encoding="UTF-8" indent="yes" method="xml" omit-xml-declaration="yes" />

 <xsl:template match="/">
<!--  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xml:base="http://isawnyu.github.com/isaw-papers-awdl/pelagios/isaw-papers-pelagios.rdf"> -->
  <xsl:apply-templates select="//h:a[contains(@href,'http://pleiades.stoa.org/places')]"/>
<!--
 </rdf:RDF>
-->
</xsl:template>

<xsl:template match="h:a">
<rdf:Description rdf:ID="isaw-papers-{$ipnum}-reference-{position()}">
 <rdf:type rdf:resource="http://www.openannotation.org/ns/Annotation"/>
 <oac:hasBody rdf:resource="{@href}"/>
 <oac:hasTarget rdf:resource="http://dlib.nyu.edu/awdl/isaw/isaw-papers/{$ipnum}/#{ancestor::h:p/@id}"/>
 <dcterms:creator rdf:resource="http://isaw.nyu.edu/" />
 <dcterms:title>Reference in ISAW Papers <xsl:value-of select="$ipnum"/> to "<xsl:apply-templates/>".</dcterms:title>
</rdf:Description>
</xsl:template>

</xsl:stylesheet><!-- and (contains(@href,'pleiades')) -->
