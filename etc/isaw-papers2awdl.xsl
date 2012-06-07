<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
	version="1.0"
        xmlns="http://www.w3.org/1999/xhtml"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:dyn="http://exslt.org/dynamic"
	xmlns:h="http://www.w3.org/1999/xhtml"
        xmlns:exsl="http://exslt.org/common"
        extension-element-prefixes="exsl dyn"
	exclude-result-prefixes="h dyn exsl xsl" >

 <xsl:output encoding="UTF-8" indent="yes" method="xml" omit-xml-declaration="no" cdata-section-elements=""/>
 <xsl:preserve-space elements="h:script"/>

<xsl:template match="/">
 <xsl:apply-templates/>
</xsl:template>

 <xsl:template match="@*|node()">
  <xsl:copy>
   <xsl:apply-templates select="@*|node()"/>
  </xsl:copy>
 </xsl:template>

 <xsl:template match="h:head">
  <xsl:element name="head">
   <xsl:apply-templates select="@*"/>
  
   <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
  
   <script src="http://isawnyu.github.com/awld-js/lib/requirejs/require.min.js" type="text/javascript"></script>
   
   <script src="http://isawnyu.github.com/awld-js/awld.js?{$autoinit}" type="text/javascript"></script>

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
   <xsl:apply-templates select="document('./head.xml')"/>
   <xsl:apply-templates/>
   
   <hr/>
   <div class="section">
    <strong>Links to Definitions of Referenced Entities</strong>
    <p class="textindent0" style="background:#aaa;margin:1em;padding:.3em">As part of the editorial process, ISAW Papers adds links to publicly available descriptions of people, places, documents and other resources that are referenced in the articles it publishes. The purpose of these links is to aid in the searching and organization of all ISAW Papers articles. They are not the responsibility of the authors, nor is ISAW Papers responsible for the content of the linked resources.</p>
    
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
 
