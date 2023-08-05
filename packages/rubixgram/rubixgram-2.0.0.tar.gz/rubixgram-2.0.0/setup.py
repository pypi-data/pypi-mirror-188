#!/bin/python
from setuptools import setup, find_packages
requires = ["requests", "urllib3", "pycryptodome","colorama","tinytag"]
version = '2.0.0'

setup(
    name="rubixgram",
    version=version,
    description="RubiDark Library For Rubika Messenger",
    long_description_content_type="text/markdown",
    url="https://github.com/mester-root/rubx",
    author="Mohamad Dark",
    author_email="mr.mohamad.dark@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet",
        "Topic :: Communications",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    keywords=["messenger","python2","python","python3","api","self","Rubx","Rubika", "RubiDark","rubix","rubikax","rubika","bot","robot","library","rubikalib","rubikalibrary","rubika.ir","libraryRubiDark","m.rubika.ir"],
    python_requires="~=3.5",
    packages=find_packages(),
    zip_safe=False,
    install_requires=requires
)