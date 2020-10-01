import re

from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, srcFile):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("args"): args = token["args"]

        httpLibs = ['httplib.urlretrieve', 'urllib.request.urlopen','urllib.urlopen', 'urllib2.urlopen', 'requests.get', 'requests.post', 'urllib.request.Request']
        
        if tokenType == "variable" and token.__contains__("valueSrc") and token.__contains__("args"):
            args = token['args']
            valueSrc = token['valueSrc']

            if valueSrc in httpLibs and len(args) > 0:
                if args[0] is not None:
                    
                    url = find_url_from_string(args[0])
                    if len(url) > 0 and url[0].split("://")[0] != "https": 
                        action_upon_detection(project_name, srcFile, lineno, 'use of HTTP without TLS', 'use of HTTP without TLS', token)

        if tokenType == "function_call" and name in httpLibs:
            if len(args) > 0 and args[0] is not None:
                
                url = find_url_from_string(args[0])
                print(url)
                if len(url) > 0 and url[0].split("://")[0] != "https":
                   
                    action_upon_detection(project_name, srcFile, lineno, 'use of HTTP without TLS', 'use of HTTP without TLS', token)

    except Exception as error: save_token_detection_exception('http only detection  '+str(error)+'  '+ str(token), srcFile)

def find_url_from_string(string): 
  
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)       
    return [x[0] for x in url] 