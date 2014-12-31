## About

tKroopy is an open source Tkinter framework for building groups of small to medium GUI applications.

Think of it as a central location where you would store all of your applications that run tasks. Be it extracting data out of your database or a handy calculator to work out how much annual leave you'll have in say 6 months time.

## Features

* Data Abstraction Layer - web2py's powerful DAL library
* Page - page system lets you flick through applications on a single window
* Table - display your data from your database with a couple of lines of code
* Console - a thread safe Text widget
* Productionisation - when applying patches to existing applications you can continue to develop applications without having to worry about preventing them from going into production

## Dependancies

tkroopy relies on a couple of additional modules:

Included:
* [pyDAL](https://github.com/web2py/pydal)

Download required:
* [py2exe](http://www.py2exe.org/) (windows) - follow install instructions

## Use

### Running

Download or fork tkroopy to your local machine, you should store it in a subfolder like tkroopy/source.

You can run using tKroopy.py in the root directory.

### Creating New Applications

Copy the /src/template.py file into the /src/Applications/ directory and build your code ontop of this module. The file name needs to be the same as the initiating class name.

### Compiling

If you want to share your applications to non-python users you can compile the code into an executable using setup.bat in the root directory (will add support for osx soon).

#### Configure Setup

The setup.bat file executes the setup.py file, there are a couple of tweeks you can make to it.

##### Test
If you wish to run a test run then leave test=True, this will output your compiled code to tkroopy/tkroopy

##### Name
You probably want to rename your application to something more meaningful, change name from 'tkroopy' to whatever you like
The compiled code will go into your root directory one up, i.e. if you have your code in tkroopy/source then

## Directory Structure

    project/
        config/       > config files
            config.ini    > general config file
        contrib/      > third party modules
        images/       > icons etc.
        logs/         > log files
        scripts/      > store any python code that cannot be compiled, e.g. ArcPy scripts
        src/
            applicatoins/ > place your applications in here
                examples/   > group your applications into subfolders
            modules/      > framework modules
                console.py    > threadsafe Text widget with vscrollbar
                hyperlink.py  > insert hyperlink into console
                page.py        > base class for all applications
                table.py      > grid view of data
            main.py       > main menu
            template.py   > use this as the template for creating your applications
            tkroopy.py    > base class for tkroopy, manages tabs (applications)
        LICENSE       > License GNU GPL v3.0
        setup.bat     > run this to execute the build script (windows)
        setup.py      > the build script, create executable version
        tKroopy.py    > the startup script
