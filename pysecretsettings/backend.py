#
# Backends for storage of app parameters and secrets
#
from typing import Any, Dict, Optional
import os.path
import stat

from .error import PySecretSettingsBackendError as BackendError
from .crypto import decrypt_dict

class PySecretSettingsBackend:
    '''
    Generic API for the settings and secrets storage
    '''

    def load(self, realm:str, key:Optional[str] = None) -> Dict[str, str]:
        '''
        realm is like a section in an INI file - use '' to get all the secrets
        in one dict of dicts.
        key is the decryption key to be used to decrypt the values associated
        with 'encrypted-' keys
        '''
        raise BackendError('Child must implement')
        return {}

    def decrypt_realms(self, data:Dict[str, Any],
            key:Optional[str]) -> Dict[str, str]:
        '''
        data is a dictionary of dictionaries
        '''
        if key is None:
            return data

        assert isinstance(key, str)
        key_bytes = key.encode(encoding='UTF-8')
        #bytes(key, 'utf-8')
        res:Dict[str, Any] = {}
        for k,v in data.items():
            if isinstance(v, dict):
                res[k] = decrypt_dict(v, key_bytes)
            else:
                res[k] = v
        return res

    def decrypt_realm(self, data:Dict[str, Any],
            key:Optional[str]) -> Dict[str, Any]:
        '''
        data is a dict
        key is the decryption key.  If None, do not try to decrypt
        '''
        if key is None:
            return data
        assert isinstance(key, str)
        key_bytes = key.encode(encoding='UTF-8')
        return decrypt_dict(data, key_bytes)
#
# Backends to store secrets in a local file
#
class FileBackend(PySecretSettingsBackend):
    '''
    Use local file to store secrets.
    Locations we search unless fully qualified path is given:
    current, then user's home dir.
    Supports enforcement of file permissions so that only user and not group or
    others can read it.
    '''
    def __init__(self, path:str, check_permissions:bool):
        '''
        path - short or a fully qualified path to the file.  In former case
        current dir and user's home is checked.
        check_permissions - check that the file is readable by user only
        decrypt - request to decrypt values associated with `encrypted-` keys.
        '''

        def find_file(file_name:str) -> str:
            '''
            Try to locate file_name:
            - first in current then
            - in user home dir.
            If starts with / or ~ - it is treated as an absolute path.
            Returns abs path to file if succeeds.  '' otherwise.
            '''

            if file_name.startswith('~'):
                # this is a home dir spec
                file_name = os.path.expanduser(file_name)
                if os.path.isfile(file_name):
                    return os.path.abspath(file_name)
                return ''

            elif file_name.startswith('/') or \
                    file_name.startswith('..') or \
                    file_name.startswith('./'):
                # this is an absolute path
                if os.path.isfile(file_name):
                    return os.path.abspath(file_name)
                return ''

            # try to find file_name at the following locations:
            for loc in ['./',  os.path.expanduser('~/')]:
                fpath = os.path.abspath(loc + file_name)
                if os.path.isfile(fpath):
                    return fpath

            return ''

        def check_file_permissions(path:str) -> str:
            '''
            Verify self.path permissions.
            Returns errmsg, '' in case of success.
            '''
            mode = os.stat(path).st_mode
            if stat.S_IMODE(mode) & (stat.S_IRGRP | stat.S_IROTH):
                return f"'{path}' is readable by group or others"

            return ''

        self.path = find_file(path)
        if not self.path:
            raise BackendError(f"Failed to find '{path}'")

        if check_permissions:
            errmsg = check_file_permissions(self.path)
            if errmsg:
                raise BackendError(errmsg)
        return

class YamlBackend(FileBackend):
    '''
    Backend to store settings in an un-encrypted
    [YAML](https://www.javatpoint.com/yaml) file
    '''

    def __init__(self, path:str, check_permissions:bool = False):
        '''
        path - short or a fully qualified path to the file.  In former case
        current dir and user's home is checked.
        check_permissions - check that the file is readable by user only
        '''
        super().__init__(path, check_permissions)
        return

    def load(self, realm:str, key:Optional[str] = None) -> Dict[str, str]:
        '''
        Load secrets dictionary from YAML file.
        realm is like a section in an INI file, use '' to get all the secrets
        in one dict.
        '''
        import yaml

        with open(self.path) as settings:
            data = yaml.load(settings, Loader=yaml.Loader)

        if isinstance(data, dict):
            if not realm:
                return self.decrypt_realms(data, key)
            elif realm not in data:
                raise BackendError(f"YAML data have no realm '{realm}'")
            data = data[realm]
            return self.decrypt_realm(data, key)

        elif isinstance(data, list):
            raise BackendError(
                "YAML secrets should be a dictionary, not a list")
        raise BackendError(
            f"YAML secrets should be a dictionary, not {type(data)}")

class IniBackend(FileBackend):
    '''
    Backend to store settings in an un-encrypted INI file
    '''

    def __init__(self, path:str, check_permissions:bool = False):
        '''
        path - short or a fully qualified path to the file.  In former case
        current dir and user's home is checked.
        check_permissions - check that the file is readable by user only
        '''
        if path is None:
            path = 'secrets.ini'
        super().__init__(path, check_permissions)
        return

    def load(self, realm:str, key:Optional[str] = None) -> Dict[str, str]:
        '''
        Load secrets dictionary from INI file.
        realm is like a section in an INI file, use '' to get all the secrets
        in one dict.
        '''
        from configparser import ConfigParser

        parser = ConfigParser()
        try:
            parser.read(self.path)
        except Exception as ex:
            raise BackendError(f"Failed to parse '{self.path}': {ex}")

        res:Dict[str, Any] = {}
        if not realm:
            for sec in parser.sections():
                res[sec] = {
                    opt: parser.get(sec, opt) for opt in parser.options(sec)
                }
            return self.decrypt_realms(res, key)
        elif realm in parser.sections():
            res = {
                opt: parser.get(realm, opt) for opt in parser.options(realm)
            }
            return self.decrypt_realm(res, key)
        raise BackendError(f"Failed to locate '{realm}' in '{self.path}'")
