
class PySecretSettingsError(Exception):
    '''
    Common parent for the package errors
    '''
    def __init__(self, msg:str):
        self.msg = msg
        return

class PySecretSettingsBackendError(PySecretSettingsError):
    '''
    Generic error to be raised by a backend
    '''
    pass
