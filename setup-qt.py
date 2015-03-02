#!/usr/bin/env python

import os
from glob import glob

package = "qspectrumanalyzer"
module = "qspectrumanalyzer"
languages = ["cs"]

print("Rebuilding PyQt resource files...")
for f in glob("{}/*.qrc".format(package)):
    os.system("pyrcc4 -o {}/qrc_{}.py {}".format(package, os.path.basename(f[:-4]), f))

print("Rebuilding PyQt UI files...")
for f in glob("{}/*.ui".format(package)):
    os.system("pyuic4 -o {}/ui_{}.py {}".format(package, os.path.basename(f[:-3]), f))

print("Updating translations...")
os.system("pylupdate4 {}/*.py -ts {}".format(package,
                                             " ".join("{}/languages/{}_{}.ts".format(package, module, lang)
                                                      for lang in languages)))
os.system("lrelease {}/languages/*.ts".format(package, module))

print("Regenerating .pyc files...")
for f in glob("{}/*.pyc".format(package)):
    os.remove(f)
__import__("{}.{}".format(package, module))
