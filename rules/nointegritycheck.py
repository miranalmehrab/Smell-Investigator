import re
from urllib.parse import urlparse

from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, imports,project_name, src_file):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("args"): args = token["args"]
            
        libs = ['urllib.request.urlretrieve','urllib.urlretrieve','urllib2.urlopen','requests.get','wget.download']

        if tokenType == "variable" and token.__contains__('valueSrc') and token.__contains__('args'):    
            if token['valueSrc'] in libs and len(token['args']) > 0:
                if isinstance(args[0], str) and is_valid_download_url(args[0]) and 'hashlib' not in imports:
                    action_upon_detection(project_name, src_file, lineno, 'no integrity check', 'no integrity check', token)
                

        elif tokenType == "function_call" and name in libs and len(args) > 0:
            if isinstance(args[0], str) and is_valid_download_url(args[0]) and 'hashlib' not in imports:
                action_upon_detection(project_name, src_file, lineno, 'no integrity check', 'no integrity check', token)
        

        elif tokenType == "function_def" and token.__contains__('return') and token.__contains__('returnArgs'):
            returnArgs = token['returnArgs']
            
            if len(returnArgs) > 0:
                if token['return'] in libs and isinstance(returnArgs[0], str) and is_valid_download_url(returnArgs[0]) and 'hashlib' not in imports:
                    action_upon_detection(project_name, src_file, lineno, 'no integrity check', 'no integrity check', token)
        

    except Exception as error: save_token_detection_exception('no integrity detection  '+str(error)+'  '+ str(token), src_file)


def is_valid_download_url(url):
    
    file_extensions = ['iso', 'tar', 'bzip2', 'zip', 'rar', 'gzip', 'gzip2', 'gz','snap', 'flatpak',
                'deb', 'rpm', 'sh', 'run', 'bin', 'exe', 'rar', '7zip', 'msi', 'bat', 'dmg', 'pacman',
                'z', 'pkg', '7z', 'arj', 'iso', 'vcd', 'toast', 'csv', 'dat', 'db', 'dbf', 'log', 'mdb', 
                'xml','sql', 'aif', 'cda', 'mid', 'midi', 'mp3', 'mpa', 'ogg', 'wma', 'wav', 'wpl', 'email',
                'eml', 'emlx', 'msg', 'oft', 'ost', 'pst', 'vcf', 'apk', 'cgi', 'pl', 'com', 'gadget', 'jar', 
                'py', 'wsf', 'fnt', 'fon', 'otf', 'ttf', 'ai','bmp', 'gif', 'ico', 'jpeg', 'hpg', 'png', 'ps',
                'svg', 'psd', 'tif', 'tiff', 'asp', 'aspx', 'cer', 'cfm', 'cgi', 'pl', 'css', 'htm', 'html',
                'js', 'jsp', 'part', 'php', 'rss', 'xhtml', 'key', 'odp', 'pps','ppt', 'pptx', 'c', 'cpp', 'h',
                'java', 'vb', 'sh', 'swift', 'xls', 'xlsm', 'xlsx', 'bak', 'sys', 'tmp','ini', 'cab', 'cfg', 'cpl',
                'cur', 'dll', 'dmp', 'drv','icns','ico','lnk','sys','doc','docx','pdf','odt','rtf','tex','txt','pwd',
                'odf','wmv','vob','swf','rm','mpeg','mpg','mp4','mp3','mov','mkv','m4v','h264','flv','avi','3gp','3g2'
            ]

    reg_url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(url))
    url = reg_url[0] if len(reg_url) > 0 else None
    if url is None: return False

    parsed_url = urlparse(url)
    
    file_path = parsed_url.path
    path_extension = file_path.split('/')[-1]
    path_extension = path_extension.split('.')[-1]
    if path_extension in file_extensions: return True
    
    file_query = parsed_url.query
    query_extension = file_query.split('=')[-1] if len(file_query.split('=')) > 0 else query_extension
    query_extension = query_extension.split('.')[-1]  if len(file_query.split('.')) > 0 else query_extension
    if query_extension in file_extensions: return True

    elif 'file' in file_query: return True
    elif 'File' in file_query: return True
    elif 'FILE' in file_query: return True

    else: return False
