# -*- coding: utf-8 -*-#
import Tkinter
import logging
import sys, os

# set basedir for testing this application
if '__file__' in globals():
    basedir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    sys.path.append(basedir)

    format = '%(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s'
    logging.basicConfig(format=format, level=logging.NOTSET)

# import when running tkroopy
import src.modules.page as page
from contrib.pydal import DAL, Field

db = page.Page.db
log = logging.getLogger(__package__)

class template(page.Page):
    """
    App Template - Enter a description of the Application here
    """
    production = False

    def __init__(self, root, name, *args, **kwargs):
        """
        Initiate the Application
        You can code widgets here but to not initialise any data. Loading data
        should be done in the load method.
        """
        page.Page.__init__(self, root, name)

        # Displayed in the main menu
        self.title = 'Application Title'
        self.models()
        # Enter any instance variables here.

        # Enter any tk widgets here.

    @staticmethod
    def models():
        # Documentation on DAL
        # http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer
        pass

    def load(self):
        """
        Initiates the application when the button is clicked in the main menu
        """
        # Remove any previous instances of application UI
        try:
            self.frame_main.pack_forget()
            self.frame_main.destroy()
        except:
            pass

        ## self.interior is the frame which sits inside the canvas to enable vertical scrolling
        self.frame_main = Tkinter.Frame(self.interior)
        self.frame_main.pack()

        # Any code here will be run when the application is started from the main menu



if __name__ == '__main__':
    root = Tkinter.Tk()
    main = Template(root, "App Template")
    main.load()
    main.pack(expand="true", fill="both")
    root.mainloop()
    exit()


# ------ END OF FILE ----