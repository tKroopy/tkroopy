# -*- coding: utf-8 -*-#
import Tkinter
import logging
import webbrowser
from functools import partial
import sys, os

if '__file__' in globals():
    basedir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..')

try:
    import src.modules.tab as tab
    import src.modules.table as table
except:
    sys.path.append(r'%s\src' % basedir)
    import modules.tab as tab
    import modules.table as table

    format = '%(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s'
    logging.basicConfig(format=format, level=logging.NOTSET)

log = logging.getLogger(__package__)

class Template(tab.Tab):
    """
    App Template - Enter a description of the Application here
    """
    production = False

    def __init__(self, root, name, basedir, *args, **kwargs):
        """
        Initiate the Application
        You can code widgets here but to not initialise any data. Loading data
        should be done in the load method.
        """
        tab.Tab.__init__(self, root, name, basedir)

        # Displayed in the main menu
        self.title = 'Application Title'

        # Enter any instance variables here.

        # Enter any tk widgets here.

    def load(self):
        """
        Initiates the application when the button is clicked in the main menu
        """
        tab.Tab.load(self)

        # Any code here will be run when the application is started from the main menu



if __name__ == '__main__':
    root = Tkinter.Tk()
    main = Template(root, "App Template", basedir)
    main.load()
    main.pack(expand="true", fill="both")
    root.mainloop()
    exit()


# ------ END OF FILE ----