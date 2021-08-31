# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## 0.1.0 - 2021-08-31

First release. No code changes, only a README update.


## 0.0.2 - 2021-07-14

Pre-release version. Fixed an issue with `versioneer` that occurs when doing a PEP517 style build:  
https://github.com/python-versioneer/python-versioneer/issues/193


## 0.0.1 - 2021-07-14

Pre-release version. Packaged the module properly and added automatic versioning with `versioneer`. Using `versionner` rather than the more recent `setuptools-scm` because we want to retain compatibility with Python 2.7.