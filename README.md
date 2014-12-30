## About

tKroopy is an open source Tkinter framework for building groups of small to medium GUI applications. 

Think of it as a central location where you would store all of your applications that run tasks. Be it extracting data out of your database or a handy calculator to work out how much annual leave you'll have in say 6 months time.

## Features

* DAL

## Dependancies

tkroopy relies on a couple of additional modules:

* [pyDAL](https://github.com/web2py/pydal) - comes with tkroopy in site-packages folder.
You will need additional libraries to connect to an existing database, see [here](http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#Dependencies).

To compile code:
* [py2exe](http://www.py2exe.org/) (windows) - follow install instructions

## Use

### Running

Download or fork tkroopy to your local machine, you can then run using tKroopy.py in the root directory.

### Creating New Applications

Copy the /src/template.py file into the /src/Applications/ directory and build your code ontop of this module. The file name needs to be the same as the initiating class name.

### Compiling

If you want to share your applications internally to non-python users you can compile the code into an executable using setup.bat in the root directory. 

## Directory Structure

    project/
        config/       > config files
            config.ini    > general config file
        images/       > icons etc.
        logs/         > YYYYMMDD.log files
        scripts/      > store any python code that cannot be compiled, e.g. ArcPy scripts
        src/
            applicatoins/ > place your applications in here
            modules/      > framework modules
                console.py    > threadsafe Text widget with vscrollbar
                hyperlink.py  > insert hyperlink into console
                tab.py        > base class for all applications
                table.py      > grid view of data
            main.py       > main menu
            template.py   > use this as the template for creating your applications
            tkroopy.py    > base class for tkroopy, manages tabs (applications)
        LICENSE       > License GNU GPL 3.0
        setup.bat     > run this to execute the build script (windows)
        setup.py      > the build script, create executable version
        tKroopy.py    > the startup script
