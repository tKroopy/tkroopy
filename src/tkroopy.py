# -*- coding: utf-8 -*-#

# References
# -----------------------------
# - Tkinter class :: http://sebsauvage.net/python/gui/
# - MVC Influence :: https://bitbucket.org/driscollis/medialocker
# - Tabs :: http://code.activestate.com/recipes/577261-python-tkinter-tabs/
# - Hyperlink :: http://effbot.org/zone/tkinter-text-hyperlink.htm
# - scrollbars :: http://stackoverflow.com/questions/9561030/vertical-and-horizontal-scrollbars-on-tkinter-widget
# - tkFileDialog :: http://tkinter.unpythonic.net/wiki/tkFileDialog
# -----------------------------

import logging

log = logging.getLogger(__package__)

# UI Base Class
import Tkinter, tkMessageBox

# Import Controllers
import main

class tKroopy(Tkinter.Tk):

    def __init__(self, basedir):
        Tkinter.Tk.__init__(self)

        self.title('tKroopy - Home')
        self.name = "Home"
        self.minsize(700, 400)
        self.geometry("700x550")
        #self.iconbitmap(r'%s\tkRoopy.ico' % basedir)

        # Config
        import ConfigParser, os

        config = ConfigParser.ConfigParser()
        config.read(os.path.join(basedir,'config/config.ini'))

        # Check if production environment
        self.production = config.get('Version', 'Production')

        # Create the class variables for the tabs
        self.tabs = {}
        self.buttons = {}
        self.current_tab = None

        self.tab_order = ['Home']
        self.tab_order_index = 0

        # Header
        self.frame_header = Tkinter.Frame(self)
        self.frame_header.pack(fill="both")

        # Header - buttons
        frame_header_buttons = Tkinter.Frame(self.frame_header)
        frame_header_buttons.pack(side="left")

        self.btn_back = Tkinter.Button(frame_header_buttons, text="<", command=self.back)
        self.btn_back.grid(row=0, column=0, padx=(5,0), pady=5)
        self.btn_back.config(state="disabled")

        self.btn_forward = Tkinter.Button(frame_header_buttons, text=">", command=self.forward)
        self.btn_forward.grid(row=0, column=1, padx=(0,5), pady=5)
        self.btn_forward.config(state="disabled")

        btn_main = Tkinter.Button(frame_header_buttons, text="Home", command=(lambda name=self.name: self.switch_tab(name)))
        btn_main.grid(row=0, column=3, padx=5, pady=5)

        # Header - Status (Stage/Production)
        frame_header_status = Tkinter.Frame(self.frame_header)
        frame_header_status.pack(side="right")


        # Main - Menu
        frame_main = main.Main(self, name="Home", bg="white")
        frame_main.pack(expand="true", fill="both")

        self.add(frame_main, btn_main)
        self.switch_tab("Home")

    def add(self, tab, button):
        # hide the tab on init
        tab.pack_forget()

        # add it to the list of tabs
        # pack the button to the left most of self
        self.tabs[tab.name] = tab
        # add it to the list of buttons
        self.buttons[tab.name] = button

    def switch_tab(self, name):
        if self.current_tab:
            # hide the current tab
            self.tabs[self.current_tab].pack_forget()
        # add the new tab to the display
        self.tabs[name].pack(expand="true", fill="both")
        self.tabs[name].load()
        self.title("tKroopy - %s" % self.tabs[name].title)
        # set the current tab to itself
        self.current_tab = name

        # Maintains the back/forward order
        #log.debug('switch to: %s - %s' % (self.tab_order, self.tab_order_index))
        if self.current_tab == 'Home':
            self.tab_order = ['Home']
            self.tab_order_index = 0
            self.btn_back.config(state="disabled")
        elif name in self.tab_order:
            self.tab_order_index = self.tab_order.index(name)
        else:
            self.tab_order.append(self.current_tab)
            self.tab_order_index = self.tab_order.index(self.current_tab)
            self.btn_back.config(state="normal")

        if self.tab_order.index(self.current_tab) == len(self.tab_order):
            self.btn_forward.config(state="disabled")

    def back(self):
        #log.debug('before: %s - %s' % (self.tab_order, self.tab_order_index))
        self.tab_order_index = self.tab_order.index(self.current_tab)-1
        #log.debug('switch to: %s' % self.tab_order[self.tab_order_index])
        self.switch_tab(self.tab_order[self.tab_order_index])
        #self.btn_forward.config(state="normal")
        #log.debug('after: %s - %s' % (self.tab_order, self.tab_order_index))


    def forward(self):
        #log.debug('before: %s - %s' % (self.tab_order, self.tab_order_index))
        self.tab_order_index = self.tab_order.index(self.current_tab)+1
        #log.debug('switch to: %s' % self.tab_order[self.tab_order_index])
        self.switch_tab(self.tab_order[self.tab_order_index])
        #log.debug('after: %s - %s' % (self.tab_order, self.tab_order_index))


# ------ END OF FILE ----
