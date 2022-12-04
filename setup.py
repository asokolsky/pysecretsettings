from setuptools import find_packages, setup

setup(
    name='pysecretsettings',
    packages=find_packages(include=['pysecretsettings']),
    version='0.0.1',
    description='A python library to access application settings and secrets',
    long_description='''This module offers a unified API for storing parameters
and/or secrets in INI or YAML files, with optional field encryption''',
    long_description_content_type="text/markdown",
    author='Alex Sokolsky',
    author_email='asokolsky@gmail.com',
    install_requires=[],
    setup_requires=[],
    tests_require=[],
    test_suite='tests',
    url='https://github.com/asokolsky/pysecretsettings',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    keywords='settings secrets',
    project_urls={
        'Source': 'https://github.com/asokolsky/pysecretsettings',
        'Tracker': 'https://github.com/asokolsky/pysecretsettings/issues',
    },
)
