# PySecretSettings Samples

How to pass secrets to a Python program?

* [command line is a bad choice](https://stackoverflow.com/questions/3830823/hiding-secret-from-command-line-parameter-on-unix)
because it is ... hardly a secret.
* environment is marginally better - use
[python-dotenv](https://pypi.org/project/python-dotenv/) for that.
* standard input or reading from a file is a better option

## sample1

[sample1.py](sample1.py) is an application with settings (and secrets) stored
in a local file `sample1.ini`.  Secrets are encrypted using
[AES Encryption and Decryption Online Tool(Calculator)](https://www.devglan.com/online-tools/aes-encryption-decryption).
Encryption key is saved and then provided to the application via standard
input:

```
(venv) alex@latitude7490:~/Projects/pysecretsettings/doc/ > python3 sample1.py
settings without decryption:  {
    "foo": "bar",
    "bar": "123",
    "port": "8080",
    "encrypted-password": "dOcV7/WfKO9RaK0Y6BbeQg=="
}
Enter encryption key:
decrypted settings:  {
    "foo": "bar",
    "bar": "123",
    "port": "8080",
    "password": "BigB1gSecret"
}
```

Alternatively the encryption key can be fed from a file:

```
(venv) alex@latitude7490:~/Projects/pysecretsettings/doc/ > python3 sample1.py<secret
settings without decryption:  {
    "foo": "bar",
    "bar": "123",
    "port": "8080",
    "encrypted-password": "dOcV7/WfKO9RaK0Y6BbeQg=="
}
decrypted settings:  {
    "foo": "bar",
    "bar": "123",
    "port": "8080",
    "password": "BigB1gSecret"
}
```
