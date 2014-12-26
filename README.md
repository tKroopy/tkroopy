## tkroopy

Free open source tkinter framework for grouping many small to medium applications together.

## Use

Copy the /src/template.py file into the /src/Applications/ direcotry and build your code ontop of this module. The file name needs to be the same as the initiating class name.

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
            main.py       > main menu, manages tabs (applications)
            template.py   > use this as the template for creating your applications
            tkroopy.py    > base class for tkroopy
        LICENSE       > License GNU GPL 3.0
        setup.bat     > run this to execute the build script (windows)
        setup.py      > the build script, create executable version
        tKroopy.py    > the startup script
