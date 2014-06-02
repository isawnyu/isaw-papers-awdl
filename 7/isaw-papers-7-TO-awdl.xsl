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

 <xsl:output encoding="UTF-8" indent="yes" method="xml" omit-xml-declaration="no" cdata-section-elements="" doctype-public = "" />
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
   
   <script src="http://isawnyu.github.com/awld-js/awld.js?autoinit" type="text/javascript"></script>

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
   <div id="isaw_papers_header" style="text-align:justified; background:#aaa;margin:1em;padding:2em">
    <p class="textindent0">This article is available at the URI <a href="{//*[@rel = 'canonical']/@href}"><xsl:value-of select="//*[@rel = 'canonical']/@href"/></a> as part of the NYU Library's <a href="http://dlib.nyu.edu/awdl">Ancient World Digital Library</a> in partnership with the <a href="http://isaw.nyu.edu/">Institute for the Study of the Ancient World</a> (ISAW). More information about <i>ISAW Papers</i> is available on the <a href="http://isaw.nyu.edu/publications/isaw-papers">ISAW</a> website.</p>
    
    <p class="textindent0" style="text-align:center;margin-top:1em">Except where noted, ©2014 <xsl:value-of select="//*[@property='cc:attributionName']"/>; distributed under the terms of the Creative Commons Attribution License<br/>
     <a href="http://creativecommons.org/licenses/by/3.0/">
      <img alt="Creative Commons License" style="border-width:0;margin-top:1em;align:center" src="http://i.creativecommons.org/l/by/3.0/88x31.png" /> 
     </a>
    </p>
</div>
   <xsl:apply-templates/>
   
 </xsl:element>
</xsl:template>

<xsl:template match="h:a[@class='reference']">
 <xsl:element name="a">
  <xsl:apply-templates select="@*"/>
  <xsl:attribute name="target" >_blank</xsl:attribute>
  <xsl:apply-templates/>
 </xsl:element>
</xsl:template>

<xsl:template match="h:a[@class='subject']">
 <xsl:element name="a">
  <xsl:apply-templates select="@*"/>
  <xsl:attribute name="target" >_blank</xsl:attribute>
  <xsl:apply-templates/>
 </xsl:element>
</xsl:template>
 
 <xsl:template match="h:p[@id]">
  
  <xsl:element name="p">
   <xsl:attribute name="onmouseover">document.getElementById('<xsl:value-of select="@id"/>anchor').style.display=''</xsl:attribute>
   <xsl:attribute name="onmouseleave">document.getElementById('<xsl:value-of select="@id"/>anchor').style.display='none'</xsl:attribute>
   <xsl:apply-templates select="@*"/>

   <a id="{@id}anchor" class="id_link" style="color:aaa;display:none" href="#{@id}">[☞<xsl:text> </xsl:text> <xsl:value-of select="@id"/>]</a><xsl:text> </xsl:text><xsl:apply-templates/>
   </xsl:element>
 </xsl:template>


<xsl:template match="h:a[@rel='contents']">
 <a rel="toc" href="http://dlib.nyu.edu/awdl/isaw/isaw-papers/7/"><xsl:apply-templates/></a>
</xsl:template>

</xsl:stylesheet>
 
