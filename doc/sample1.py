#
# sample use of pysecretsettings
# Load, decrypt and print the settings read from `sample1.ini
#
from getpass import getpass
from sys import stdin
import json

from pysecretsettings import PySecretSettings

def read_encryption_key(prompt:str) -> str:
    '''
    Read some secret from stdin.  If stdin is interactive, display a prompt.
    '''
    if stdin.isatty():
        pw = getpass(prompt=prompt, stream=None)
    else:
        line = stdin.readline()
        pw = line.rstrip()
    return pw

def main() -> None:
    '''
    Load, decrypt and display the settings
    '''
    settings = PySecretSettings('sample1.ini')
    settings.load('settings')
    print('settings without decryption: ', json.dumps(settings.secrets, indent=4))

    key = read_encryption_key('Enter encryption key: ')
    settings.load('settings', key)
    print('decrypted settings: ', json.dumps(settings.secrets, indent=4))
    return


if __name__ == '__main__':
    main()
