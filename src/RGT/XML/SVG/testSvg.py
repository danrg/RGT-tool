from RGT.XML.SVG.Util import *

if __name__ == '__main__':
    impl = SvgDOMImplementation()
    doc = impl.createSvgDocument()
#    root= doc.documentElement
#    lineNode= doc.createElement('line')
#    root.appendChild(lineNode)
    root= doc.documentElement
    lineNode= doc.createLineNode(5, 10)
    lineNode.setStyle('stroke: #000000; fill:#00ff00;')
    cssNode= doc.createJavaScriptNode("""circle {
           stroke: #006600;
           fill:   #00cc00;
        }""")
    lineNode.setOnMouseOut('llaa')
    lineNode.setSystemLanguage('en')
    root.appendChild(cssNode)
    root.appendChild(lineNode)
    print doc.toxml()
    
#    impl2= getDOMImplementation()
#    xmlDoc= impl.createDocument(None, "svg", None)
#    root2= xmlDoc.documentElement
#    lineNode= xmlDoc.createElement('line')
#    root2.appendChild(lineNode)
#    print xmlDoc.toxml()