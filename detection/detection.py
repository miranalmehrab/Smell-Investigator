import json

from rules.xss import Xss
from rules.cipher import Cipher
from rules.ipbinding import IpBinding
from rules.debugflag import DebugFlag
from rules.tempdir import TmpDirectory
from rules.dynamicode import DynamicCode
from rules.httponly import HttpWithoutTLS
from rules.yamlload import YamlOperations 
from rules.ignexcept import IgnoreException
from rules.sqlinjection import SqlInjection
from rules.assertstat import AssertStatement 
from rules.emptypassword import EmptyPassword
from rules.nocertificate import NoCertificate
from rules.nointegritycheck import NoIntegrity
from rules.filepermission import FilePermission
from rules.hardcodedsecret import HardcodedSecret
from rules.deserialization import Deserialization
from rules.commandinjection import CommandInjection

from operations.save_token_exceptions import save_token_detection_exception
from operations.save_token_exceptions import save_token_loading_exception


def get_imported_modules_from_source_code(tokens):

    imported_modules = []
    for token in tokens:
        try: 
            token = json.loads(token)
            if token['type'] == 'import':
                imported_modules.append(token['og'])

        except Exception as error: print(str(error))
    return imported_modules


def detection(tokens, project_name, src_file_name):

    tokens = tokens.splitlines()
    imported_modules = get_imported_modules_from_source_code(tokens)
    
    xss = Xss()
    cipher = Cipher()
    yaml = YamlOperations()
    debug_flag = DebugFlag()
    tmp_dir = TmpDirectory()
    ip_binding = IpBinding()
    dynamic_code = DynamicCode()
    no_integrity = NoIntegrity()
    sql_injection = SqlInjection()
    hard_secret = HardcodedSecret()
    empty_password = EmptyPassword()
    no_certificate = NoCertificate()
    file_permission = FilePermission()
    deserialization = Deserialization()
    http_without_tls = HttpWithoutTLS()
    ignore_exception = IgnoreException()
    assert_statement = AssertStatement()
    command_injection = CommandInjection()

    for token in tokens:
        try:
            token = json.loads(token)
            
            xss.detect_smell(token, project_name, src_file_name)
            yaml.detect_smell(token, project_name, src_file_name)
            cipher.detect_smell(token, project_name, src_file_name)
            tmp_dir.detect_smell(token, project_name, src_file_name)
            debug_flag.detect_smell(token, project_name, src_file_name)
            ip_binding.detect_smell(token, project_name, src_file_name)
            hard_secret.detect_smell(token, project_name, src_file_name)
            dynamic_code.detect_smell(token, project_name, src_file_name)
            sql_injection.detect_smell(token, project_name, src_file_name)
            empty_password.detect_smell(token, project_name, src_file_name)
            no_certificate.detect_smell(token, project_name, src_file_name)
            deserialization.detect_smell(token, project_name, src_file_name)
            file_permission.detect_smell(token, project_name, src_file_name)
            http_without_tls.detect_smell(token, project_name, src_file_name)
            ignore_exception.detect_smell(token, project_name, src_file_name)
            assert_statement.detect_smell(token, project_name, src_file_name)
            command_injection.detect_smell(token, project_name, src_file_name)
            no_integrity.detect_smell(token, imported_modules, project_name, src_file_name)

        except Exception as error: 
            save_token_loading_exception(str(token)+'  '+str(error),src_file_name)
        
        