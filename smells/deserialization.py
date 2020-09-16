from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, srcFile):
    try:

        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]

        insecureMethods = ['pickle.loads', 'pickle.load', 'pickle.Unpickler', 'cPickle.loads', 'cPickle.load', 'cPickle.Unpickler', 'marshal.loads', 'marshal.load', 
                            'xml.etree.cElementTree.parse', 'xml.etree.cElementTree.iterparse','xml.etree.cElementTree.fromstring','xml.etree.cElementTree.XMLParser',
                            'xml.etree.ElementTree.parse', 'xml.etree.ElementTree.iterparse', 'xml.etree.ElementTree.fromstring', 'xml.etree.ElementTree.XMLParser',
                            'xml.sax.expatreader.create parser', 'xml.dom.expatbuilder.parse', 'xml.dom.expatbuilder.parseString', 'xml.sax.parse', 'xml.sax.parseString', 
                            'xml.sax.make parser','xml.dom.minidom.parse','xml.dom.minidom.parseString', 'xml.dom.pulldom.parse','xml.dom.pulldom.parseString','lxml.etree.parse',
                            'lxml.etree.fromstring','lxml.etree.RestrictedElement','xml.etree.GlobalParserTLS, lxml.etree.getDefaultParser, lxml.etree.check docinfo'
                        ]

        if tokenType == "variable":
            if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]
            if token.__contains__("args"): args = token["args"]
            if valueSrc in insecureMethods and args is not None and len(args) > 0:
                action_upon_detection(project_name, srcFile, lineno, 'insecure_data_diserialization', 'insecure data diserialized', token)

        elif tokenType == "function_call":
            if token.__contains__("name"): name = token["name"]
            if token.__contains__("args"): args = token["args"]
            if name in insecureMethods and args is not None and len(args) > 0: 
                action_upon_detection(project_name, srcFile, lineno, 'insecure_data_diserialization', 'insecure data diserialized', token)
        
        elif tokenType == "function_def":
            if token.__contains__("return"): funcReturn  = token["return"]
            if token.__contains__("returnArgs"): returnArgs = token["returnArgs"]
            if funcReturn in insecureMethods and returnArgs is not None and len(returnArgs) > 0: 
                action_upon_detection(project_name, srcFile, lineno, 'insecure_data_diserialization', 'insecure data diserialized', token)
    
    except Exception as error: save_token_detection_exception('deserialization detection  '+str(error)+'  '+ str(token), srcFile)
    