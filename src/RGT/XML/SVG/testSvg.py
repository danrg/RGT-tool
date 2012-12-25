from RGT.XML.SVG.svgDOMImplementation import SvgDOMImplementation
from RGT.XML.SVG import Util

if __name__ == '__main__':
    impl = SvgDOMImplementation()
    doc = impl.createSvgDocument()
#    root= doc.documentElement
#    lineNode= doc.createElement('line')
#    root.appendChild(lineNode)
    root= doc.documentElement
    root.setX('10px')
    root.setOnError('lalal')
    root.setFill('red')
    lineNode= doc.createLineNode(5, 10)
    lineNode.setStyle('stroke: #000000; fill:#00ff00;')
    recNode= doc.createRectNode(10, 12, 1000, 500)
    cssNode= Util.createCssStyleNode(doc, """circle {
           stroke: #006600;
           fill:   #00cc00;
        }""")
    jsNode= Util.createJavaScriptNode(doc, 'function la(d){d= 1; console(d)}')
#    lineNode.setOnMouseOut('llaa')
#    lineNode.setSystemLanguage('en')
    descNode= doc.createDescNode()
    descNode.setId('weeep')
    #lineNode2= doc.createLineNode(4,9)
    #descNode.appendChild(lineNode2)
    descNode.setText('la')
    textNode= doc.createSvgTextNode()
    textNode.setText('ok weee')
    textNode.setText('lllll')
    textNode.setId('textParaEu')
    filterNode= doc.createFilterNode()
    blendNode= doc.createFeBlendNode()
    blendNode.setIn('1 10 12 142 1423 1423 542')
    filterNode.appendChild(blendNode)
    symbolNode= doc.createSymbolNode()
    root.appendChild(cssNode)
    root.appendChild(lineNode)
    root.appendChild(descNode)
    root.appendChild(recNode)
    root.appendChild(textNode)
    root.appendChild(filterNode)
    root.appendChild(symbolNode)
    root.appendChild(jsNode)
    print doc.toxml()
    
#    impl2= getDOMImplementation()
#    xmlDoc= impl.createDocument(None, "svg", None)
#    root2= xmlDoc.documentElement
#    lineNode= xmlDoc.createElement('line')
#    root2.appendChild(lineNode)
#    print xmlDoc.toxml()