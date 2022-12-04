#
#
#
import os.path
#from typing import List
import unittest

from pysecretsettings import PySecretSettings, PySecretSettingsError


def test_file(fname:str) -> str:
    '''
    Given a short file name return a fq path.
    Important if the tests are started from the parent dir.
    '''
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dirname, fname)

class PySecretSettings_test(unittest.TestCase):

    def test_nonexistent_file(self) -> None:
        '''
        Test behavior of a misconfigured object
        '''
        file_name = 'test-file-absent.ini'
        with self.assertRaises(PySecretSettingsError) as ctx:
            PySecretSettings(file_name)

        self.assertEqual(
            ctx.exception.msg, f"Failed to find '{file_name}'")
        return

    def test_yaml_unencrypted(self) -> None:
        '''
        Test positive simple YAML file
        '''
        settings = PySecretSettings(test_file('test-simple.yaml'))
        data = settings.load('')
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data['sample-string'], str)
        self.assertIsInstance(data['sample-string-multi-line-nl-ignored'], str)
        self.assertIsInstance(data['sample-string-multi-line-nl-included'], str)
        self.assertIsInstance(data['sample-path'], str)
        self.assertIsInstance(data['sample-integer'], int)
        self.assertIsInstance(data['sample-integer-octal'], int)
        self.assertIsInstance(data['sample-integer-hexa'], int)
        self.assertIsInstance(data['sample-float'], float)
        self.assertIsInstance(data['sample-float-exp'], float)
        self.assertIsInstance(data['sample-boolean'], bool)
        self.assertIsInstance(data['sample-boolean-YesNo'], bool)
        self.assertIsInstance(data['sample-boolean-TrueFalse'], bool)
        self.assertIsInstance(data['sample-boolean-OnOff'], bool)
        self.assertIsInstance(data['sample-dict'], dict)
        self.assertIsInstance(data['sample-list'], list)

        self.assertEqual(
            data['sample-string-multi-line-nl-ignored'].count('\n'),
            1)
        self.assertGreater(
            data['sample-string-multi-line-nl-included'].count('\n'),
            1)
        return

    def test_yaml_secrets(self) -> None:
        '''
        Test positive simple YAML file
        '''
        settings = PySecretSettings(test_file('test-simple.yaml'))

        # attempt to read data before load should fail
        with self.assertRaises(PySecretSettingsError) as ctx:
            settings['key']
        self.assertEqual(ctx.exception.msg, "secrets not loaded")

        # proceed as usual
        settings.load('secrets')
        key = str(settings['key'])
        #assert key is not None
        self.assertTrue(key)

        # now load and decrypt section `realm1`
        settings.load('realm1', key)
        self.assertEqual(
            settings['decrypted-password1'], settings['password1'])
        self.assertEqual(
            settings['decrypted-password2'], settings['password2'])

        return

    def test_ini_secrets(self) -> None:
        '''
        Test positive simple YAML file
        '''
        fname = test_file('test-secrets.ini')
        settings = PySecretSettings(fname)
        # the key is not encrypted - get it from the file
        settings.load('secrets')
        key = settings['key']

        # now load and decrypt section `realm1`
        settings.load('realm1', key)

        self.assertEqual(
            settings['decrypted-password1'], settings['password1'])
        self.assertEqual(
            settings['decrypted-password2'], settings['password2'])
        return
