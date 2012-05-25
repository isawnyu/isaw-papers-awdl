<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:dyn="http://exslt.org/dynamic"
    xmlns:exsl="http://exslt.org/common"
    extension-element-prefixes="exsl dyn"
	version="1.0"
	exclude-result-prefixes="h dyn"
	xmlns:h="http://www.w3.org/1999/xhtml">
 <xsl:output encoding="UTF-8" indent="yes" method="xml" omit-xml-declaration="no" cdata-section-elements=""/>
 <xsl:preserve-space elements="h:script"/>
<xsl:template match="/">
 <html xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.w3.org/1999/xhtml http://www.w3.org/MarkUp/SCHEMA/xhtml-rdfa-1.xsd"
  xml:lang="en"
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:bibo="http://purl.org/ontology/bibo/"
  xmlns:cc="http://creativecommons.org/ns#"
  xmlns:dcterms="http://purl.org/dc/terms/"
  xmlns:dcmitype="http://purl.org/dc/dcmitype/"
  xmlns:foaf="http://xmlns.com/foaf/0.1"
  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
  >
  <xsl:apply-templates select="//h:head"/>
	<xsl:apply-templates select="//h:body"/>
 </html>
</xsl:template>


 <xsl:template match="h:head">
  <xsl:element name="head">
   <xsl:apply-templates select="@*"/>
   <xsl:text disable-output-escaping="yes">
    <![CDATA[<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js"> </script>]]>
   </xsl:text>

   <script type="text/javascript">
  function show_id_links() {
if ($('.id_link').css('display') == "none")
$('.id_link').show();
else
$('.id_link').hide();
}

  function show_references() {
 $('.reference').css('border-bottom','thin dotted gray');
 }
   </script>
   <xsl:apply-templates/>
  </xsl:element>
  </xsl:template>

 <xsl:template match="h:body">
  <xsl:element name="body">
   <xsl:apply-templates select="@*"/>
   <center style="background:#aaa;margin:1em;padding:.3em">
    <p style="width:80%">This article is available at the URI http://dlib.nyu.edu/awdl/isaw/isaw-papers/1 as part of the NYU Library's <a href="http://dlib.nyu.edu/awdl" style="text-decoration:underline">Ancient World Digital Library</a> in partnership with the <a href="http://isaw.nyu.edu/" style="text-decoration:underline">Institute for the Study of the Ancient World</a> (ISAW).  More information about <i>ISAW Papers</i> is available on the <a href="http://isaw.nyu.edu/publications/isaw-papers" style="text-decoration:underline">ISAW</a> website. Please note that while the content of this article will not change, its appearance and interaction with other resources will  develop over time.</p>
    <a href="http://creativecommons.org/licenses/by/3.0/"> 
  <img alt="Creative Commons License" style="border-width:0;margin-top:1em" src="http://i.creativecommons.org/l/by/3.0/88x31.png" /> 
    </a>
    <p onclick="show_id_links();">Click here to show/hide internal links to individual paragraphs, tables, etc.</p>
 </center>
 <xsl:apply-templates/>
   
   <hr/>
   <div class="section">
    <strong>Links to Definitions of Referenced Entities</strong>
    <p class="textindent0" style="background:#aaa;margin:1em;padding:.3em">As part of the editorial process, ISAW Papers adds links to publicly available descriptions of people, places, documents and other resources that are referenced in the articles it publishes. The purpose of these links is to aid in the searching and organization of all ISAW Papers articles. They are not the responsibility of the authors, nor is ISAW Papers responsible for the content of the linked resources.</p>
    <p onclick="show_references();" class="textindent0" style="background:#aaa;margin:1em;padding:.3em">Click here to show all links to descriptions of referenced entities in the text of this article. When showing, links are highlighted by a dotted underline.</p>
    
    <h2>Geographic Entities</h2>
    <xsl:if test="//*[@typeof='dcterms:Location']">
    <ol>
     <xsl:apply-templates select="//*[@typeof='dcterms:Location']" mode="enhancer"><xsl:sort select="."/></xsl:apply-templates>
    </ol>
    </xsl:if>
   
   
    <xsl:if test="//*[@typeof='foaf:Person']">
    <h2>People</h2>
    <ol>
     <xsl:apply-templates select="//*[@typeof='foaf:Person']" mode="enhancer"><xsl:sort select="."/></xsl:apply-templates>
    </ol>
    </xsl:if>
    
    <xsl:if test="//*[@typeof='dcmitype:Text']">
    <h2>Texts</h2>
    <ol>
     <xsl:apply-templates select="/h:html/h:body//*[@typeof='dcmitype:Text']" mode="enhancer" ><xsl:sort select="."/></xsl:apply-templates>
    </ol>
    </xsl:if>

    <xsl:if test="//*[@typeof='dcmitype:PhysicalObject']">
    <h2>Objects</h2>
    <ol>
     <xsl:apply-templates select="/h:html/h:body//*[@typeof='dcmitype:PhysicalObject']" mode="enhancer" ><xsl:sort select="."/></xsl:apply-templates>
    </ol>
    </xsl:if>
    
    <xsl:if test="//*[@typeof='nm:hoard']">
    <h2>Coin Hoards</h2>
    <ol>
     <xsl:apply-templates select="//*[@typeof='nm:hoard']" mode="enhancer" ><xsl:sort select="."/></xsl:apply-templates>
    </ol>
    </xsl:if>
    
    <xsl:if test="//*[@typeof='nm:typology_entry']">
    <h2>Coin Types</h2>
    <ol>
     <xsl:apply-templates select="//*[@typeof='nm:typology_entry']" mode="enhancer" ><xsl:sort select="."/></xsl:apply-templates>
    </ol>
    </xsl:if>
    
   </div>
 </xsl:element>
</xsl:template>

 <xsl:template match="@*|node()">
  <xsl:copy>
   <xsl:apply-templates select="@*|node()"/>
  </xsl:copy>
 </xsl:template>


<xsl:template match="h:a[@class='reference']">
 <xsl:element name="a">
  <xsl:apply-templates select="@*"/>
  <xsl:attribute name="target" >_new</xsl:attribute>
  <xsl:apply-templates/>
 </xsl:element>
</xsl:template>

<xsl:template match="h:a[@class='subject']">
 <xsl:element name="a">
  <xsl:apply-templates select="@*"/>
  <xsl:attribute name="target" >_new</xsl:attribute>
  <xsl:apply-templates/>
 </xsl:element>
</xsl:template>
 
 <xsl:template match="h:p[@id]">
  
  <xsl:element name="p">
   <xsl:apply-templates select="@*"/>
   <a class="id_link" style="color:aaa;display:none" href="#{@id}">[☞<xsl:text> </xsl:text> <xsl:value-of select="@id"/>]</a><xsl:text> </xsl:text><xsl:apply-templates/>
   </xsl:element>
 </xsl:template>

<xsl:template match="*[@typeof]" mode="enhancer">
 <li>
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
    <xsl:if test="descendant-or-self::*[@href]"><span style="color:gray"> as defined or described at <a><xsl:attribute name="href"><xsl:value-of select="descendant-or-self::*[@href]/@href"/></xsl:attribute><xsl:attribute name="target">_new</xsl:attribute><xsl:value-of select="descendant-or-self::*[@href]/@href"/></a>.</span></xsl:if>
 </li>
</xsl:template>


</xsl:stylesheet>
 
