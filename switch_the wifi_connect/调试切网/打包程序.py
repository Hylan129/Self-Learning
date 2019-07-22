#!/usr/bin/env python
# coding=utf-8
from distutils.core import setup
import py2exe
setup(
description = 'software',
version = '0.0.1',
console=[{"script": "client.py", "icon_resources": [(1, "client.ico")]}],
options = {
'py2exe': {
'compressed': 1,
'optimize': 2,
'bundle_files': 2
}
}
)