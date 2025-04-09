# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.2.0 - 2025-04-09

Added ability to ignore channels in the outlier analysis.

### Added

- `iqrm_mask()` now has an `ignorechans` argument with a list of frequency channels to exclude from the analysis.
  Thanks to Kathryn Crowter for this addition ([#1](https://github.com/v-morello/iqrm/pull/1)).
- Version string is now exposed as `iqrm.__version__`

### Fixed

- Package is now installable with Python 3.12+, thanks to Ujjwal Panda ([#4](https://github.com/v-morello/iqrm/pull/4)).

## 0.1.0 - 2021-08-31

First release. No code changes, only a README update.


## 0.0.2 - 2021-07-14

Pre-release version. Fixed an issue with `versioneer` that occurs when doing a PEP517 style build:  
https://github.com/python-versioneer/python-versioneer/issues/193


## 0.0.1 - 2021-07-14

Pre-release version. Packaged the module properly and added automatic versioning with `versioneer`. Using `versionner` rather than the more recent `setuptools-scm` because we want to retain compatibility with Python 2.7.