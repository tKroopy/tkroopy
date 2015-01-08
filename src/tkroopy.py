# -*- coding: utf-8 -*-#

# References
# -----------------------------
# - Tkinter class :: http://sebsauvage.net/python/gui/
# - MVC Influence :: https://bitbucket.org/driscollis/medialocker
# - Pages :: http://code.activestate.com/recipes/577261-python-tkinter-tabs/
# - Hyperlink :: http://effbot.org/zone/tkinter-text-hyperlink.htm
# - scrollbars :: http://stackoverflow.com/questions/9561030/vertical-and-horizontal-scrollbars-on-tkinter-widget
# - tkFileDialog :: http://tkinter.unpythonic.net/wiki/tkFileDialog
# -----------------------------

import logging

log = logging.getLogger(__package__)

# UI Base Class
import Tkinter, tkMessageBox

# Import Controllers
import applications.main as main
import modules.status_bar as status_bar

class tKroopy(Tkinter.Tk):
    def __init__(self, basedir):
        Tkinter.Tk.__init__(self)

        self.title('tKroopy - Home')
        self.name = "Home"
        self.minsize(700, 400)
        self.geometry("700x550")
        self.iconbitmap(r'%s\images\tKroopy.ico' % basedir)

        # Config
        import ConfigParser, os

        config = ConfigParser.ConfigParser()
        config.read(os.path.join(basedir,'config/config.ini'))

        self.basedir = basedir

        # Check if production environment
        self.production = config.get('Version', 'Production')

        # Create the class variables for the pages
        self.pages = {}
        self.buttons = {}
        self.current_page = None

        self.page_order = ['Home']
        self.page_order_index = 0

        # Header
        self.frame_header = Tkinter.Frame(self)
        self.frame_header.pack(side="top", fill="both")

        # Header - buttons
        frame_header_buttons = Tkinter.Frame(self.frame_header)
        frame_header_buttons.pack(side="left")

        self.btn_back = Tkinter.Button(frame_header_buttons, text="<", command=self.back)
        self.btn_back.grid(row=0, column=0, padx=(5,0), pady=5)
        self.btn_back.config(state="disabled")

        self.btn_forward = Tkinter.Button(frame_header_buttons, text=">", command=self.forward)
        self.btn_forward.grid(row=0, column=1, padx=(0,5), pady=5)
        self.btn_forward.config(state="disabled")

        btn_main = Tkinter.Button(frame_header_buttons, text="Home", command=(lambda name=self.name: self.change_page(name)))
        btn_main.grid(row=0, column=3, padx=5, pady=5)

        # Header - Status (Stage/Production)
        frame_header_status = Tkinter.Frame(self.frame_header)
        frame_header_status.pack(side="right")


        # Main - Menu
        frame_main = main.Main(self, name="Home", bg="white")
        frame_main.pack(side='top', expand="true", fill="both")

        self.add_page(frame_main, btn_main)
        self.change_page("Home")
        
        # Footer
        frame_footer = Tkinter.Frame(self, height='30')
        frame_footer.pack(side='bottom', fill='x')

        # Status Bar
        self.status = status_bar.Status_Bar(frame_footer)
        self.status.pack(side='left')

    def add_page(self, page, button):
        # hide the page on init
        page.pack_forget()

        # add it to the list of pages
        # pack the button to the left most of self
        self.pages[page.name] = page
        # add it to the list of buttons
        self.buttons[page.name] = button

    def change_page(self, name):
        """
        Change Page
        Give a page name, will switch to the page given
        """
        if self.current_page:
            # hide the current page
            self.pages[self.current_page].pack_forget()
        # add the new page to the display
        self.pages[name].pack(expand="true", fill="both")
        self.pages[name].load()
        self.title("tKroopy - %s" % self.pages[name].title)
        # set the current page to itself
        self.current_page = name

        # Maintains the back/forward order
        #log.debug('switch to: %s - %s' % (self.page_order, self.page_order_index))
        if self.current_page == 'Home':
            self.page_order = ['Home']
            self.page_order_index = 0
            self.btn_back.config(state="disabled")
        elif name in self.page_order:
            self.page_order_index = self.page_order.index(name)
        else:
            self.page_order.append(self.current_page)
            self.page_order_index = self.page_order.index(self.current_page)
            self.btn_back.config(state="normal")

        if self.page_order.index(self.current_page) == len(self.page_order):
            self.btn_forward.config(state="disabled")

    def back(self):
        """
        Back Navigation
        When going multiple pages deep user can click the back button to head
        towards the Main Menu.
        """
        #log.debug('before: %s - %s' % (self.page_order, self.page_order_index))
        self.page_order_index = self.page_order.index(self.current_page)-1
        #log.debug('switch to: %s' % self.page_order[self.page_order_index])
        self.change_page(self.page_order[self.page_order_index])
        #self.btn_forward.config(state="normal")
        #log.debug('after: %s - %s' % (self.page_order, self.page_order_index))


    def forward(self):
        """
        Forward Navigation
        When user hits the back button but wishes to go back (again) they can
        use the forward button to go to the previous page.
        (Currently disabled)
        """
        #log.debug('before: %s - %s' % (self.page_order, self.page_order_index))
        self.page_order_index = self.page_order.index(self.current_page)+1
        #log.debug('switch to: %s' % self.page_order[self.page_order_index])
        self.change_page(self.page_order[self.page_order_index])
        #log.debug('after: %s - %s' % (self.page_order, self.page_order_index))


# ------ END OF FILE ----
