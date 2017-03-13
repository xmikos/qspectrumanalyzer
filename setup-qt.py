#!/usr/bin/env python

import os, shutil
from glob import glob

package = "qspectrumanalyzer"
languages = ["cs"]

print("Rebuilding PyQt resource files...")
for f in glob("{}/*.qrc".format(package)):
    os.system("pyrcc5 -o {}/qrc_{}.py {}".format(package, os.path.basename(f[:-4]), f))

print("Rebuilding PyQt UI files...")
for f in glob("{}/*.ui".format(package)):
    os.system("pyuic5 -o {}/ui_{}.py {}".format(package, os.path.basename(f[:-3]), f))

print("Changing compiled UI files from PyQt5 to Qt.py wrapper...")
os.system("sed -i 's/^from PyQt5 import/from Qt import/g' {}/ui_*.py".format(package))

print("Updating translations...")
lang_files = " ".join("{}/languages/{}_{}.ts".format(package, package, lang) for lang in languages)
os.system("pylupdate5 {}/*.py -ts {}".format(package, lang_files))
os.system("lrelease {}/languages/*.ts".format(package))

print("Regenerating .pyc files...")
shutil.rmtree("{}/__pycache__".format(package), ignore_errors=True)
for f in glob("{}/*.pyc".format(package)):
    os.remove(f)
__import__("{}.__main__".format(package))
