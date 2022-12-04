import os.path
from typing import Any, Dict, Optional

from .backend import PySecretSettingsBackend, IniBackend, YamlBackend
from .error import PySecretSettingsError, PySecretSettingsBackendError as BackendError

def path2backend(path:str, check_permissions:bool) -> PySecretSettingsBackend:
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    if ext in ('.yaml', '.yml'):
        return YamlBackend(path, check_permissions)
    elif ext in ('.ini'):
        return IniBackend(path, check_permissions)
    try:
        # start guessing...is it YAML?
        return YamlBackend(path, check_permissions)
    except BackendError:
        pass
    try:
        # keep guessing...is it INI?
        return IniBackend(path, check_permissions)
    except BackendError:
        pass
    # I give up
    raise BackendError(f"Failed to identify backend from '{path}'")

class PySecretSettings:
    '''
    Generic API to retrieve secrets, with or without encryption.
    '''

    def __init__(self, arg:Any, **args:Dict[str,Any]):
        '''
        arg can be a backend or a string - in the latter case we will guess the
        backend
        '''

        self.backend:PySecretSettingsBackend
        if isinstance(arg, str):
            self.backend = path2backend(
                arg, bool(args.get('check_permissions', False)))
        elif isinstance(arg, PySecretSettingsBackend):
            self.backend = arg
        else:
            raise BackendError(
                f"Failed to identify backend from '{arg}'")
        self.secrets:Optional[Dict[str, str]] = None
        return

    def load(self, realm:str, key:Optional[str] = None) -> Dict[str, str]:
        '''
        Use backend to load the secrets into self.secrets
        '''
        if self.backend is None:
            raise PySecretSettingsError('backend not set')
        self.secrets = self.backend.load(realm, key)
        return self.secrets

    def get(self, key:str, default:Any = None) -> Any:
        if self.secrets is None:
            raise PySecretSettingsError('secrets not loaded')
        return self.secrets.get(key, default)

    def __getitem__(self, key:str) -> Any:
        '''
        enable use of []
        '''
        return self.get(key)
