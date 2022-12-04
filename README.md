# pysecretsettings README

A python library to access settings and secrets.

This module offers a unified API for storing parameters
and/or secrets in INI or YAML files, with optional field encryption.

Storage backends:

* [YAML](https://pyyaml.org/wiki/PyYAMLDocumentation)/
[INI](https://docs.python.org/3/library/configparser.html) file with
un-encrypted settings
* YAML/INI file with encrypted settings

To have the values encrypted you can use
[AES Encryption and Decryption Online Tool(Calculator)](https://www.devglan.com/online-tools/aes-encryption-decryption)

Reasonable encryption defaults:

* Cipher Mode: CBC
* Key size (bits): 128 - will require a 16 char secret.
* Initialization vector: none
* Text format: base64

## Usage scenarios

Access to the secrets may be done by:

* a human;
* software executed locally, possibly with no Internet access;
* by github actions, e.g.
[encrypted secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets?tool=cli),
also consider github repo secrets via
[gh secret](https://cli.github.com/manual/gh_secret).

## Sample use

See the [doc](./doc/) folder.

## TODO

More backends to consider in the future:

* [vault](https://www.hashicorp.com/products/vault) via
[HVAC](https://hvac.readthedocs.io/en/stable/usage/index.html)
* [credstash](https://github.com/fugue/credstash)
* [BlackBox](https://github.com/StackExchange/blackbox)
* [git-secret](https://github.com/sobolevn/git-secret)
* [git-crypt](https://github.com/AGWA/git-crypt)
* [dot env](https://www.realpythonproject.com/3-ways-to-store-and-read-credentials-locally-in-python/)
