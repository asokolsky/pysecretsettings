#
#
#
import os.path
#from typing import List
import unittest


#from logger import log
from pysecretsettings import (
    FileBackend,
    IniBackend,
    YamlBackend,
    decrypt_dict,
    PySecretSettingsError
)

def test_file(fname:str) -> str:
    '''
    Given a short file name return a fq path
    '''
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dirname, fname)

class FileBackend_test(unittest.TestCase):
    '''
    class FileBackend test cases

    to run all these: `python3 -m unittest backend_test.py`
    to run just one: `python3 -m unittest backend_test.FileBackend_test.test_nonexistent_file`
    '''
    test_file_name = 'test-file-backend'

    def tearDown(self) -> None:
        '''
        remove the test_file_name from all the possible locations
        '''
        for loc in ('./',  os.path.expanduser('~/')):
            fpath = os.path.abspath(loc + self.test_file_name)
            if os.path.isfile(fpath):
                os.remove(fpath)
        return

    def test_nonexistent_file(self) -> None:
        '''
        Test behavior of misconfigured object
        '''
        with self.assertRaises(PySecretSettingsError) as ctx:
            FileBackend(self.test_file_name, False)

        self.assertEqual(
            ctx.exception.msg, f"Failed to find '{self.test_file_name}'")
        return

    def create_test_file(self, dir:str, mask:int = 0o666) -> str:
        path = dir + self.test_file_name

        def opener(path:str, flags:int) -> int:
            '''
            Custom opener to set file permissions
            '''
            return os.open(path, flags, mask)

        with open(path, 'w', opener=opener) as f:
            f.write(f'# {path} \n')
            # the descriptor is automatically closed when fh is closed
            #
        return path

    def test_file_permissions(self) -> None:
        '''
        Test behavior of misconfigured object
        '''
        # create file in the current dir but wrong permissions
        path = self.create_test_file('./')

        with self.assertRaises(PySecretSettingsError) as ctx:
            FileBackend(self.test_file_name, True)

        self.assertEqual(
            ctx.exception.msg,
            f"'{os.path.abspath(path)}' is readable by group or others")
        return

    def test_file_current_dir(self) -> None:
        '''
        Test file in current dir
        '''
        # create file in the current dir
        path = self.create_test_file('./')

        # check fully qualified path
        backend = FileBackend(path, False)
        self.assertEqual(os.path.abspath(path), backend.path)

        # check path NOT specified
        backend = FileBackend(self.test_file_name, False)
        self.assertEqual(os.path.abspath(path), backend.path)
        return

    def test_file_home_dir(self) -> None:
        '''
        Test file in current dir
        '''
        # create file in home dir
        path = self.create_test_file(os.path.expanduser('~/'))
        backend = FileBackend(path, False)
        self.assertEqual(os.path.abspath(path), backend.path)

        # check path specified using ~/
        backend = FileBackend(f'~/{self.test_file_name}', False)
        self.assertEqual(os.path.abspath(path), backend.path)

        # check path NOT specified
        backend = FileBackend(self.test_file_name, False)
        self.assertEqual(os.path.abspath(path), backend.path)
        return

class YamlBackend_test(unittest.TestCase):
    '''
    class YamlBackend test cases

    to run all these: `python3 -m unittest backend_test.py`
    to run just one: `python3 -m unittest backend_test.YamlBackend_test.test_nonexistent_file`
    '''

    def test_nonexistent_file(self) -> None:
        '''
        Test behavior of misconfigured object
        '''
        fname = 'does-not-exist.yaml'
        with self.assertRaises(PySecretSettingsError) as ctx:
            YamlBackend(fname)

        self.assertEqual(
            ctx.exception.msg, f"Failed to find '{fname}'")
        return

    def test_yaml_list(self) -> None:
        '''
        Test behavior of malformed secrets file
        '''
        fname = test_file('test-list.yaml')
        backend = YamlBackend(fname)
        with self.assertRaises(PySecretSettingsError) as ctx:
            backend.load('')

        self.assertEqual(
            ctx.exception.msg, "YAML secrets should be a dictionary, not a list")
        return

    def test_yaml_simple(self) -> None:
        '''
        Test positive simple YAML file
        '''
        fname = test_file('test-simple.yaml')
        backend = YamlBackend(fname)
        data = backend.load('')
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

    def test_yaml_flow(self) -> None:
        '''
        Test positive flow-style YAML file
        '''
        fname = test_file('test-flow.yaml')
        backend = YamlBackend(fname)
        data = backend.load('')

        self.assertIsInstance(data, dict)
        self.assertIsInstance(data['sample-string'], str)
        self.assertIsInstance(data['sample-dict'], dict)
        self.assertIsInstance(data['sample-list'], list)
        return


class IniBackend_test(unittest.TestCase):
    '''
    class IniBackend test cases

    to run all these: `python3 -m unittest backend_test.py`
    to run just one: `python3 -m unittest backend_test.IniBackend_test.test_nonexistent_file`
    '''

    def test_nonexistent_file(self) -> None:
        '''
        Test behavior of misconfigured object
        '''
        fname = test_file('does-not-exist.ini')
        with self.assertRaises(PySecretSettingsError) as ctx:
            IniBackend(fname)

        self.assertEqual(
            ctx.exception.msg, f"Failed to find '{fname}'")
        return

    def test_ini_simple(self) -> None:
        '''
        Test positive simple INI file
        '''
        fname = test_file('test-simple.ini')
        backend = IniBackend(fname)
        data = backend.load('')
        self.assertIsInstance(data, dict)

        data1 = backend.load('realm1')
        self.assertIsInstance(data1, dict)

        data2 = backend.load('realm2')
        self.assertIsInstance(data2, dict)

        self.assertEqual(data['realm1'], data1)
        self.assertEqual(data['realm2'], data2)

        self.assertEqual(data1['username'], 'alice')
        self.assertEqual(data1['password'], "1-`~!@#$%^&*()_+[]{},.<>/?")

        self.assertEqual(data2['username'], 'bob')
        self.assertEqual(data2['password'], 'bar')
        return

    def test_ini_secrets(self) -> None:
        '''
        Test positive INI file with secrets
        '''
        fname = test_file('test-secrets.ini')
        backend = IniBackend(fname)
        data = backend.load('')
        self.assertIsInstance(data, dict)

        data1 = backend.load('realm1')
        self.assertIsInstance(data1, dict)

        data2 = backend.load('realm2')
        self.assertIsInstance(data2, dict)

        self.assertEqual(data['realm1'], data1)
        self.assertEqual(data['realm2'], data2)

        self.assertEqual(data1['username'], 'alice')
        self.assertTrue(data1['encrypted-password1'])
        self.assertTrue(data1['encrypted-password2'])

        self.assertEqual(data2['username'], 'bob')
        self.assertTrue(data2['encrypted-password'])

        secrets = backend.load('secrets')
        key = secrets['key']
        key_bytes = bytes(key, 'utf-8')

        decrypted1 = decrypt_dict(data1, key_bytes)
        self.assertEqual(
            decrypted1['password1'], decrypted1['decrypted-password1'])
        self.assertEqual(
            decrypted1['password2'], decrypted1['decrypted-password2'])

        decrypted2 = decrypt_dict(data2, key_bytes)
        self.assertEqual(
            decrypted2['password'], decrypted2['decrypted-password'])
        return


if __name__ == '__main__':
    unittest.main()
