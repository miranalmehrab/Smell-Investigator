def detect(token):
    
    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("args"): args = token["args"]
        
    libs = ['urllib.urlretrieve','urllib2.urlopen','requests.get','wget.download']
    download = ['iso', 'tar', 'tar.gz', 'tar.bzip2', 'zip', 'rar', 'gzip', 'gzip2', 'deb', 'rpm', 'sh', 'run', 'bin', 'exe', 'zip', 'rar', '7zip', 'msi', 'bat']

    if name in libs and args:
        urls = args[0].split(".")
        extension = urls[len(urls)-1]

        if extension in download:
            warning = 'possible no integrity check at line '+ str(lineno)
            print(warning)
            
            # check exisitng imports if haslib or pygpgme not found then tell no checking!
            