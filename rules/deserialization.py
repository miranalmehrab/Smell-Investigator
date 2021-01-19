# from fuzzywuzzy import fuzz
from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:

        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): token_type = token["type"]

        insecure_methods = ['pickle.loads', 'pickle.load', 'pickle.Unpickler', 'cPickle.loads', 'cPickle.load', 'cPickle.Unpickler', 'marshal.loads', 'marshal.load', 
                            'xml.etree.cElementTree.parse', 'xml.etree.cElementTree.iterparse','xml.etree.cElementTree.fromstring','xml.etree.cElementTree.XMLParser',
                            'xml.etree.ElementTree.parse', 'xml.etree.ElementTree.iterparse', 'xml.etree.ElementTree.fromstring', 'xml.etree.ElementTree.XMLParser',
                            'xml.sax.expatreader.create_parser', 'xml.dom.expatbuilder.parse', 'xml.dom.expatbuilder.parseString', 'xml.sax.parse', 'xml.sax.parseString', 
                            'xml.sax.make_parser','xml.dom.minidom.parse','xml.dom.minidom.parseString', 'xml.dom.pulldom.parse','xml.dom.pulldom.parseString','lxml.etree.parse',
                            'lxml.etree.fromstring','lxml.etree.RestrictedElement','xml.etree.GlobalParserTLS', 'lxml.etree.getDefaultParser', 'lxml.etree.check docinfo'
                        ]

        if token['type'] == 'import':
            if token.__contains__('og'):
                for method in insecure_methods:
                    if is_sublist_of_another_list(token['og'].split('.'), method.split('.')):
                        action_upon_detection(project_name, src_file, lineno, 'insecure deserialization', 'insecure deserialization', token)
                        break

        elif token_type == "variable" and token.__contains__("valueSrc") and token["valueSrc"] in insecure_methods:
            action_upon_detection(project_name, src_file, lineno, 'insecure deserialization', 'insecure deserialization', token)

        elif token_type == "function_call":
            if token.__contains__("name") and token["name"] in insecure_methods: 
                action_upon_detection(project_name, src_file, lineno, 'insecure deserialization', 'insecure deserialization', token)
        
            if token.__contains__("args") and len(token["args"]) > 0:
                for arg in token["args"]:
                    if arg in  insecure_methods: 
                        action_upon_detection(project_name, src_file, lineno, 'insecure deserialization', 'insecure deserialization', token)
        

        elif token_type == "function_def" and token.__contains__("return") and token["return"] is not None:
            for func_return in token["return"]:
                if func_return in insecure_methods:
                    action_upon_detection(project_name, src_file, lineno, 'insecure deserialization', 'insecure deserialization', token)
    
    except Exception as error: save_token_detection_exception('deserialization detection  '+str(error)+'  '+ str(token), src_file)

def is_sublist_of_another_list(smaller_list, bigger_list):
    for item in smaller_list:
        if item not in bigger_list: 
            return False

    return True