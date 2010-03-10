import libxml2

#for url in doc.xpathEval('//@xmlUrl'):
#print url.content

def xmlToMatch(xml):    
    found = xml.xpathEval('/match/team')
    found.get_children
    
xmldoc = libxml2.parseFile('../doc/sampleMatch.xml').xpathev
xmlToMatch(xmldoc)