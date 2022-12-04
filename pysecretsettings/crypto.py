from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from typing import Dict

from .error import PySecretSettingsError

#
# This is convenient BUT must be reducing security of the entire solution(?)
# Looks like this is an assumption used in
# https://www.devglan.com/online-tools/aes-encryption-decryption
#
iv = bytearray([0] * AES.block_size)

def encrypt_str(input:str, key:bytes) -> str:
    '''
    Encrypt the input string using the key.
    Returns a base64 presentation of the result.
    '''
    input_bytes = bytes(input, 'utf-8')
    out_bytes = encrypt_bytes(input_bytes, key)
    return b64encode(out_bytes).decode('utf-8')

def encrypt_bytes(input:bytes, key:bytes) -> bytes:
    '''
    Encrypt the input bytes using the key.
    Returns encrypted bytes.
    '''
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return cipher.encrypt(pad(input, AES.block_size))


def decrypt_str(input:str, key:bytes) -> str:
    '''
    Given a b64 encoded string - decrypt it using the given key.
    Returns a string
    '''
    ciphertext = b64decode(input)
    text = decrypt_bytes(ciphertext, key)
    res = text.decode()
    return res


def decrypt_bytes(input:bytes, key:bytes) -> bytes:
    '''
    Given a b64 encoded string - decrypt it using the given key.
    Returns a string
    '''
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    text = cipher.decrypt(input)
    text = unpad(text, AES.block_size)
    return text


def decrypt_dict(input:Dict[str, str], key:bytes) -> Dict[str, str]:
    '''
    For every key in `input`:
      if key starts with `encrypted-XXX` - decrypt its value,
      save it under key `XXX`
    Encryption: AES
    Cipher mode: CBC
    Key size: 128 bits
    Init vector: none
    Secret key: 1234567890123456 - should be 16, 24 or 32 bytes long
    (respectively for *AES-128*, *AES-192* or *AES-256*).
    '''

    if len(key) not in [16, 24, 32]:
        raise PySecretSettingsError(f"Bad decryption key length {len(key)} - should be 16 or 24 or 32")

    key_prefix = 'encrypted-'
    res:Dict[str, str] = {}
    for k,v in input.items():
        if k.startswith(key_prefix):
            nk = k[len(key_prefix):]
            if not nk:
                raise PySecretSettingsError(f"Bad key '{k}' in '{input}'")
            nv = decrypt_str(v, key)
            res[nk] = nv
        else:
            res[k] = v

    return res
