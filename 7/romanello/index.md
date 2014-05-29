# Mining Citations, Linking Texts

## [Matteo Romanello]()

Canonical citations are the standard way of citing primary sources (i.e., the
ancient texts) in Classics: the ability to read them, which requires knowing
what numerous abbreviations stand for, is part of the early training of
any classicist. Having an expert system to capture automatically these citations
and their meaning is one of the aims of the project of which the research
presented in this paper is part. The desire for such a system has existed for
a considerable amount of time [@crane_cyberinfrastructure_2009, 26] but has yet
to be solved [@romanello_singap; @Romanello2013]. 

Such a system has great potential both for scholars in Classics and for the
study of Classics as a discipline: capturing the citations of ancient texts that
are contained in journal articles, commentaries, monographs and other secondary
sources, allows us, for example, to track over time how and how often texts were
studied, essential pieces of information for a data-driven study of the
discipline and its evolution.

Another possible use of the system is to display related bibliographic
references within a reading environment for ancient texts. The examples that are
used in this paper are taken from work that has been done to provide the GapVis
interface of the Hellespont project[^hell] with such a functionality (see Fig.
1). One of the goals of the project is to create an enhanced virtual reading
environment for one specific section of Thucydides' *Histories*, the so-called
"Pentecontaetia" (Thuc. 1,89 to 1,118). The references that are displayed in the
secondary literature view of the reading interface are mined automatically from
JSTOR and are shown together with links to the full text of the journal article
as well as to the cited passage in the Perseus digital library [@Romanello2012]. 

[^hell]: The Hellespont Project: Integrating Arachne and Perseus, http://hellespont.dainst.org/

<!--...add some stuff...-->

### Figure 1: Secondary literature view of the GapVis-based reading interface of the Hellespont project.
	
<img src="hellespont_seclit.png" width="90%" />

## Mining Citations: Extraction and Disambiguation

<!--Before going into more details concerning the ontological modelling of canonical texts and citations, let us consider briefly how the extraction of such citations from texts is performed. -->

Extracting citations requires performing two different tasks. First, the strings
that constitute the citation are captured. Second, the referent of that citation
is established---the specific section of text to which the citation refers. In Natural
Language Processing (NLP) jargon these two steps are called respectively Named
Entity Recognition (or extraction) and Named Entity Disambiguation. 

My approach to citation extraction (see Fig. 2, no. 1 and 2) is
essentially based on state-of-the-art NER techniques with the only difference
being what it takes to adapt these techniques to the new domain [@Romanello2013]. Instead of
considering only the usual named entities (NEs)--such as
names of people, places and organizations--I treat as NEs the different
components of a citation in addition to any mention of ancient authors and works
occurring in the context that surrounds the citation itself. For this purpose
four distinct entities were identified: `aauthor`, `awork`, `refauwork` and
`refscope`.<!-- perhaps explain what they are? --> In its current definition,
a citation is a relation between any two entities, where one is always the
indication of the citation's scope (i.e. `refscope`) and the other can be any of
the other entities (i.e. `aauthor`, `awork` and `refauwork`). 

### Figure 2: Diagram showing the various phases of mining canonical citations from texts.

<img src="extraction_steps.png" width="90%" />

Once captured, citations need to be disambiguated: this is done by assigning to
each citation its corresponding CTS URN. What this means in practice is that,
for instance, the citation "Hell. 3.3.1-4" of the example showed in Fig. 2 (no.
3) is mapped to its corresponding URN,
`urn:cts:greekLit:tlg0032.tlg001:3.3.1-3.3.4`. Designed to become the equivalent
of canonical citations in a digital environment, CTS URNs are a kind of
identifiers that follows the Uniform Resource Name standard and was developed
within the Multitext Homer project as part of the CITE architecture to make it
possible to "identify and retrieve digital representations of texts"
[@hmt-doku-ctsurns][^1].

[^1]: To date one of the main adopters of this technology is the Perseus project that has built on top of it to provide several functionalities of its digital library and catalog [internal ref?].

## A Knowledge Base of Canonical Texts

NER systems of this kind typically require and rely on a surrogate of domain
knowledge, such as a gazetteer or a knowledge base, to support both the
extraction and disambiguation of NEs<!--, and even more so in the case of open
domain applications-->. To support the disambiguation of canonical citations
such a knowledge base needs to contain, for example, all possible abbreviations
of the name of an author or the title of a work, possibly in multiple languages
if working on multi-lingual corpora.  Since the texts we are dealing with are
canonical it is possible to use this knowledge base to store, in addition to
abbreviations, detailed information about the citable structures of each
text
such as, for example, how many books are contained in Thucydides'
*Histories*, how many chapters are contained in book 1 etc.  Being able to query
this sort of information allows one to validate the automatically extracted
citations, thus making it possible to identify, if not to recover, those citations
that are just *impossible*. An example of this phenomenon is the string "Thuc.
5. 14. 1. 41.": although it looks as a plausible citation, it is not a valid one
as the work here referred to--Thucydides' *Histories*--is made of three, not
four, citable, hierarchical levels, (i.e. book/chapter/section). Such errors are
very common when working with OCRed texts where the lack of structural markup
causes, as in this case, the footnote number to be mistakenly interpreted as
being part of the canonical citation "Thuc. 5. 14. 1". 

<!-- 
my KB:
underlying ontological model -> HuCit
get data from CWKB and the Perseus Digital Library via it CTS-compliant interface
links to the Perseus catalog and CWKB
is stored as RDF and can be queried by using SPARQL
-->

The content in the knowledge base is structured mostly using a combination of
CIDOC-CRM and FRBRoo ontologies[^2]:  the Functional Requirements for
Bibliographic Records (FRBR) model, in particular, is suitable for modelling
information related to Classical (canonical) texts, as was showed by
@babeu_named_2007 [ref], and has influenced substantially the design of the CTS
protocol. In those few cases where these ontologies did not suffice to model the
data we have extended some of the classes they provide in what we called the
HUmanities CITation Ontology (HuCit)[^3].  

### Figure 3: The knowledge-base record for Thucydides' *Histories* serialized as RDF/Turtle. 

	@prefix ecrm: <http://erlangen-crm.org/current/> .
	@prefix efrbroo: <http://erlangen-crm.org/efrbroo/> .
	@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

	<http://data.mr56k.info/urn:cts:greekLit:tlg0003.tlg001> a efrbroo:F1_Work;
	    ecrm:P131_is_identified_by <http://data.mr56k.info/urn:cts:greekLit:tlg0003.tlg001#cts_urn>;
	    efrbroo:P102_has_title <http://data.mr56k.info/urn:cts:greekLit:tlg0003.tlg001#title>;
		owl:sameAs <http://catalog.perseus.org/catalog/urn:cts:greekLit:tlg0003.tlg001> .

	<http://data.mr56k.info/urn:cts:greekLit:tlg0003.tlg001#creation_event> a efrbroo:F27_Work_Conception;
	    efrbroo:R16_initiated <http://data.mr56k.info/urn:cts:greekLit:tlg0003.tlg001> .

	<http://data.mr56k.info/urn:cts:greekLit:tlg0003.tlg001#cts_urn> a ecrm:E42_Identifier;
	    rdfs:label "urn:cts:greekLit:tlg0003.tlg001";
	    ecrm:P2_has_type <http://data.mr56k.info/urn:cts:greekLit:tlg0003.tlg001#type_CTS_URN> .

	<http://data.mr56k.info/urn:cts:greekLit:tlg0003.tlg001#title> a efrbroo:E35_Title;
		ecrm:P139_has_alternative_form <http://data.mr56k.info/urn:cts:greekLit:tlg0003.tlg001#abbr1> .
	    rdfs:label "Der Peloponnesische Krieg"@ger,
	        "History of the Peloponnesian War"@eng,
	        "La Guerra del Peloponneso"@ita,
	        "l’Histoire de la guerre du Péloponnèse"@fre .	

	<http://data.mr56k.info/urn:cts:greekLit:tlg0003.tlg001#abbr1> a ecrm:E41_Appellation;
	    rdfs:label "Thuc.";
	    ecrm:P2_has_type <http://data.mr56k.info/type_abbreviation> .
	
As shown in Fig. 3 our record is linked to a record in the Perseus
Catalog; the CTS URN associated with the work as well as the abbreviations of its
title are explicitly modelled by using respectively the CIDOC-CRM classes
`E42_Identifier` and  `E41_Appellation`. <!-- say that the Perseus Catalog URIs
do not currently provide an RDF presentation but this will happen in the next
release -->

[^2]: The Erlangen OWL implementations of both CIDOC-CRM and FRBRoo were used: they are available respectively at <http://erlangen-crm.org/> and <http://erlangen-crm.org/efrbroo>. 

[^3]: The HuCit namespace is <http://purl.org/net/hucit>; the source code and some examples can be found in the code repository at <https://bitbucket.org/56k/hucit/>.


## Publishing Extracted Citations as Linked Open Data

Not only are canonical citations important because of their function, they are
also interesting artifacts in themselves. They were designed, well before the
advent of digital technologies, to refer to texts in a very precise and
interoperable way: *precise* because texts are the fundamental object of
philological research, therefore a scholarly discourse about texts needs an
accurate way of referring to them; *interoperable* because although texts may
exist in different editions and translations, scholars need to be able to refer
to specific sections of them without having to worry about the many possible
variations in pagination or layout each single edition may present.

If we accept that canonical citations are already a way of linking
objects--i.e., the citing text and the cited text--extracting citations
reconstructs and makes explicit links that already exist in the text. The act of
transforming citations into hyperlinks, however, may lead
to a misrepresentation of their nature and specifically of their being designed
to be interoperable: a canonical citation should not be tied to the referenced
passage in a specific edition, but should rather work as a resolvable pointer,
that can be resolved to a given portion of text in any available edition or
translation. 

Let us now consider how extracted citations are stored
and published online as Linked Open Data [@Heath2011]. By following an
approach that was largely inspired by the Pelagios Project[^pelagios], extracted
canonical citations are represented as annotations as defined by the Open
Annotation Data Model[^oac] (see Fig. 4). A new annotation is created for each
extracted citation: the string containing the citation becomes its label,
whereas the citing and the cited texts become respectively its target and
body--to use the OAC terminology--as expressed by the `oac:hasTarget` and
`oac:hasBody` properties. The property `oac:motivatedBy` is used here to clarify
the reason for creating such annotations: I chose `oac:identifying` as, in fact,
extracting citations can be seen as the act of making explicit what is the
object (i.e. text section) that is identified by a given citation.

[^pelagios]: Pelagios: Enable Linked Ancient Geodata In Open Systems, http://pelagios-project.blogspot.com. 
[^oac]: Open Annotation Data Model, http://www.openannotation.org/spec/core/.

### Figure 4: An extracted citation represented by means of the OAC ontology and serialized as RDF/Turtle.

	<http://hellespont.org/annotations/jstor#16> a oac:Annotation;
	    rdfs:label "Thuc. 1. 101";
		oac:motivatedBy oac:identifying;
	    oac:hasBody <http://data.mr56k.info/urn:cts:greekLit:tlg0003.tlg001:1.101>;
	    oac:hasTarget <http://jstor.org/stable/10.2307/268729> .



The RDF fragment that is returned when the body URI is resolved (see Fig. 5)
shows how the citation is not linked directly to the digital text but points to
an intermediate object called `hucit:TextElement`[^4]. This abstract object
identifies a citable element within the hierarchical structure of a text and is
linked via the `hucit:resolves_to` property to digital representations of the
cited passage, in this case the editions and translations available in the
Perseus Digital Library and via the Classical Works Knowledge Base (CWKB)
resolution service. It must be pointed out, however, that linking to these
resources is not, strictly and technically speaking, LOD-compliant as these URIs
do not resolve (yet) to an RDF representation of the resource identified by the
URI. However, as it has emerged clearly during the LAWDI event at which this
paper was presented, linking resources together is the first necessary step to
LOD, that it is hoped will be followed by making the underlying technology
compliant with the LOD principles. 

<!-- how is interoperability preserved? -->


[^4]: For further details about the design of HuCit see @Romanello2013a.
[^5]: Previous studies have already tackled the technical problem of how such citations can be transformed into links and have immediately seen/recognised the potential benefit for the users [refs]. 

### Figure 5: RDF/Turtle representation identified by the URI <http://data.mr56k.info/urn:cts:greekLit:tlg0003.tlg001:1.101>

	@prefix ecrm: <http://erlangen-crm.org/current/> .
	@prefix hucit: <http://purl.org/net/hucit#> .
	@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

	<http://data.mr56k.info/urn:cts:greekLit:tlg0003.tlg001:1.101> a hucit:TextElement;
	    rdfs:label "book 1, chapter 101 of Thucydides' Histories"@en,
	    ecrm:P1_is_identified_by [ a ecrm:E42_Identifier;
	            rdfs:label "urn:cts:greekLit:tlg0003.tlg001:1.101";
	            ecrm:P2_has_type <http://data.mr56k.info/CTS_URN> ];
	    hucit:is_part_of <http://data.mr56k.info/urn:cts:greekLit:tlg0012.tlg001:1>;
		hucit:precedes <http://data.mr56k.info/urn:cts:greekLit:tlg0012.tlg001:1.100>;
		hucit:precedes <http://data.mr56k.info/urn:cts:greekLit:tlg0012.tlg001:1.102>;
	    hucit:resolves_to <http://data.perseus.org/citations/urn:cts:greekLit:tlg0012.tlg001.perseus-eng1:1.1>,
	        <http://data.perseus.org/citations/urn:cts:greekLit:tlg0012.tlg001.perseus-eng2:1.1>,
	        <http://data.perseus.org/citations/urn:cts:greekLit:tlg0012.tlg001.perseus-grc1:1.1>,
			<http://cwkb.org/resolver?rft.au=Thucydides&rft.title=Historiae&rft.slevel1=1&rft.slevel2=101&rft_val_fmt=info:ofi/fmt:kev:mtx:canonical_cit&ctx_ver=Z39.88-2004> .
			



## Works Cited

<!-- notes -->
