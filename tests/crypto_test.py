from copy import copy
from typing import Any, Dict
import unittest

from pysecretsettings import (
    encrypt_str,
    decrypt_str,
    decrypt_dict
)

key = b'1234567890123456'
password = 'BigB1gSecret'
encrypted_password = 'dOcV7/WfKO9RaK0Y6BbeQg=='

class crypto_test(unittest.TestCase):
    '''
    Crypto functions unit tests
    '''
    def test_simple(self) -> None:
        '''
        Positive test of string encryption/decryption
        '''
        res = encrypt_str(password, key)
        self.assertEqual(res, encrypted_password)

        res = decrypt_str(res, key)
        self.assertEqual(res, password)

        return

    def test_decrypt_dict(self) -> None:
        '''
        Positive decrypt_dict test
        '''
        input: Dict[str, Any] = {
            'foo': 'bar',
            'username': 'bob',
            'encrypted-password': encrypted_password,
            'junk': 123
        }
        decrypted = decrypt_dict(input, key)
        expected = copy(input)
        expected['password'] = password
        del expected['encrypted-password']
        self.assertEqual(decrypted, expected)
        return
