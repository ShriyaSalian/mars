from setuptools import setup, find_packages
setup(
    name='mars',
    packages=find_packages(),
    install_requires=[
          'pythoncommons'
      ],
    version='0.0.1',
    description='Mostly Abstract Rest Structures',
    author='Ryan Berkheimer',
    author_email='rab25@case.edu',
    url='https://github.com/RBerkheimer/mars',
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: MIT Standard",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic"])
