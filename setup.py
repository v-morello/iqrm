import setuptools
import sys
import os

# See github issues:
# https://github.com/python-versioneer/python-versioneer/issues/192
# https://github.com/python-versioneer/python-versioneer/issues/193
# This is a necessary hack when doing a PEP517 style build
sys.path.append(os.path.dirname(__file__))
import versioneer

if __name__ == "__main__":
    setuptools.setup(
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
    )