import re
from urllib.parse import urlparse

from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("args"): args = token["args"]

        httpLibs = ['httplib.urlretrieve', 'urllib.request.urlopen','urllib.urlopen', 'urllib2.urlopen', 'requests.get', 'requests.post', 'urllib.request.Request']
        
        if tokenType == "variable" and token.__contains__("valueSrc") and token.__contains__("args"):
            args = token['args']
            valueSrc = token['valueSrc']

            if valueSrc in httpLibs and len(args) > 0 and args[0] is not None and is_valid_http_url(args[0]):
                action_upon_detection(project_name, src_file, lineno, 'use of HTTP without TLS', 'use of HTTP without TLS', token)
                
    
        elif tokenType == "function_call" and name in httpLibs and len(args) > 0 and args[0] is not None and is_valid_http_url(args[0]):                                     
            action_upon_detection(project_name, src_file, lineno, 'use of HTTP without TLS', 'use of HTTP without TLS', token)

        elif tokenType == "function_def" and token.__contains__('return') and token.__contains__('returnArgs'):
            func_return = token['return']
            returnArgs = token['returnArgs']

            if func_return in httpLibs and len(returnArgs) > 0 and returnArgs[0] is not None and is_valid_http_url(returnArgs[0]):           
                    action_upon_detection(project_name, src_file, lineno, 'use of HTTP without TLS', 'use of HTTP without TLS', token)

    except Exception as error: save_token_detection_exception('http only detection  '+str(error)+'  '+ str(token), src_file)

def is_valid_http_url(url): 

    reg_url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(url))
    url = reg_url[0] if len(reg_url) > 0 else None
    if url is None: return False

    parsed_url = urlparse(url)
    if parsed_url.scheme == 'http': return True
    if parsed_url.scheme == 'https': return False
    else: return False