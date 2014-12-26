# -*- coding: utf-8 -*-#
# Copyright:   see copyright in the doc folder
# License:     see license in the doc folder
#-----------------------------------------------------------------------------
#!/usr/bin/env python

from setuptools import setup
import py2exe
from glob import glob
import sys, shutil, os, zipfile
import datetime

# Switch True/False
# - test = True will compile the application into
test = False
name = 'tkroopy'

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print 'Basedir: %s' % basedir

# Copy required C++ bindings over
sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.2\bin\Microsoft.VC90.CRT')
data_files = [("Microsoft.VC90.CRT", glob(r'C:\Program Files (x86)\ArcGIS\Desktop10.2\bin\Microsoft.VC90.CRT\*.*'))]

# Include images in the build
data_files.append(('images', glob(os.path.join(basedir, r"Source\images/*.gif"))))
data_files.append(('scripts', glob(os.path.join(basedir, r"Source\scripts/*.py"))))

if test:
    # Set the destination directory
    dist_dir = os.path.join(basedir, name + ' Dev')

    # Copy config files with the build
    data_files.append(('config', glob(os.path.join(basedir, r"Source\config/*.*"))))
else:
    # Set the destination directory
    dist_dir = os.path.join(basedir, name)

    # Create zip source files and insert into the archive directory
    exclude = ['build']
    with zipfile.ZipFile(os.path.join(basedir, r'Archive\%s_%s.zip' %(name, datetime.datetime.now().strftime('%Y%m%d'))), mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        path = os.path.join(basedir, 'Source')
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in exclude]
            for file1 in files:
                zf.write(os.path.join(root, file1), os.path.relpath(os.path.join(root, file1), os.path.join(path, '..')))
                print 'Arciving: %s' % os.path.join(root, file1)

# This setup is suitable for "python setup.py develop".
setup(
        windows=[name + '.py'],
        data_files=data_files,
        options = {
            'py2exe': {
                'packages': ['src'],
                'includes': 'decimal',
                #'excludes': ['_ssl','pyreadline', 'difflib', 'doctest', 'optparse', 'pickle', 'calendar'],
                'dll_excludes':['msvcr71.dll'],
                'optimize': 0,
                'compressed': True,
                'dist_dir': dist_dir
            }
        }
)