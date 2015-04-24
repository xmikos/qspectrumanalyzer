#!/usr/bin/env python

import os, shutil
from glob import glob

package = "qspectrumanalyzer"
languages = ["cs"]

print("Rebuilding PyQt resource files...")
for f in glob("{}/*.qrc".format(package)):
    os.system("pyrcc4 -o {}/qrc_{}.py {}".format(package, os.path.basename(f[:-4]), f))

print("Rebuilding PyQt UI files...")
for f in glob("{}/*.ui".format(package)):
    os.system("pyuic4 -o {}/ui_{}.py {}".format(package, os.path.basename(f[:-3]), f))

print("Updating translations...")
lang_files = " ".join("{}/languages/{}_{}.ts".format(package, package, lang) for lang in languages)
os.system("pylupdate4 {}/*.py -ts {}".format(package, lang_files))
os.system("lrelease {}/languages/*.ts".format(package))

print("Regenerating .pyc files...")
shutil.rmtree("{}/__pycache__".format(package), ignore_errors=True)
for f in glob("{}/*.pyc".format(package)):
    os.remove(f)
__import__("{}.__main__".format(package))
