import setuptools
from setuptools import setup


# TODO: versioneer
VERSION = '0.0.1'


with open("README.md", "r") as fh:
    long_description = fh.read()


install_requires = [
    'numpy',
    'pytest',
    'pytest-cov',
]


setup(
    name='iqrm',
    url='https://bitbucket.org/vmorello/iqrm',
    author='Vincent Morello',
    author_email='vmorello@gmail.com',
    description='A minimal implementation of the IQRM interference flagging algorithm',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=VERSION,
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    license='MIT License',

    # NOTE (IMPORTANT): This means that everything mentioned in MANIFEST.in will be copied at install time 
    # to the package’s folder placed in 'site-packages'
    include_package_data=True,

    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Topic :: Scientific/Engineering :: Astronomy"
        ],
)
