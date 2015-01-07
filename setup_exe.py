# -*- coding: utf-8 -*-#

from setuptools import setup
import py2exe
from glob import glob
import sys, shutil, os, zipfile
import datetime

# Switch True/False
# - test = True will compile the application into
test = True
name = 'tkroopy'
source = 'source'

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print 'Basedir: %s' % basedir

# Copy required C++ bindings over
sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.2\bin\Microsoft.VC90.CRT')
data_files = [("Microsoft.VC90.CRT", glob(r'C:\Program Files (x86)\ArcGIS\Desktop10.2\bin\Microsoft.VC90.CRT\*.*'))]

# Include images in the build
data_files.append(('images', glob(os.path.join(basedir, r"%s\images/*.*" % source))))
data_files.append(('scripts', glob(os.path.join(basedir, r"%s\scripts/*.py" % source))))
data_files.append(('logs', glob(os.path.join(basedir, r"%s\logs/*.py" % source))))
data_files.append(('database', glob(os.path.join(basedir, r"%s\database/*.*" % source))))

if test:
    # Set the destination directory
    dist_dir = os.path.join(basedir, name + ' Dev')

    # Copy config files with the build
    data_files.append(('config', glob(os.path.join(basedir, r"%s\config/*.*" % source))))
else:
    # Set the destination directory
    dist_dir = os.path.join(basedir, name)

    # Create zip source files and insert into the archive directory
    exclude = ['build']
    with zipfile.ZipFile(os.path.join(basedir, r'Archive\%s_%s.zip' %(name, datetime.datetime.now().strftime('%Y%m%d'))), mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        path = os.path.join(basedir, name)
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in exclude]
            for file1 in files:
                zf.write(os.path.join(root, file1), os.path.relpath(os.path.join(root, file1), os.path.join(path, '..')))
                print 'Arciving: %s' % os.path.join(root, file1)

# This setup is suitable for "python setup.py develop".
setup(
        windows=[{'script':'tkroopy.py',
                    'icon_resources': [(1, 'images/tKroopy.ico')]}],
        description="tkroopy tkinter framework",
        author="James P Burke",
        license="GPL v3",
        data_files=data_files,
        #zipfile = None,
        options = {
            'py2exe': {
                'bundle_files': 2,
                'compressed':True,
                'packages': ['src', 'contrib'],
                'includes': 'decimal',
                'dll_excludes':['msvcr71.dll'],
                'optimize': 0,
                'dist_dir': dist_dir
            }
        }
)

shutil.rmtree(r'%s/build' % source)