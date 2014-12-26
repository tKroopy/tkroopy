## tkroopy


free open source tkinter framework for grouping many small to medium applications together.

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
            template.py   > use this as the template for creating your applications
        LICENSE       > License GNU GPL 3.0
        setup.bat     > run this to execute the build script (windows)
        setup.py      > the build script, create executable version
        tKroopy.py    > the startup script
