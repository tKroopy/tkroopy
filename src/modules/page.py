#-------------------------------------------------------------------------------
# Name:        Page (originally named Tab)
# Purpose:
# Source: http://code.activestate.com/recipes/577261-python-tkinter-tabs/
#
# Author:      Sunjay Varma
#
# Created:     13/05/2010
# Modified:    9/01/2014 James P Burke
#
# Copyright:   (c) Sunjay Varma 2010
# Licence:     MIT
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#-------------------------------------------------------------------------------
# Other sources
# - scrollbars :: http://stackoverflow.com/questions/9561030/vertical-and-horizontal-scrollbars-on-tkinter-widget
#-------------------------------------------------------------------------------
import Tkinter
import logging
import os, sys

log = logging.getLogger(__package__)
basedir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..').replace('library.zip', '')

from contrib.pydal import DAL, Field

class Page(Tkinter.Frame):
    """
    A base tab class - with vertical scrolling
    """

    db = DAL('sqlite://storage.db', folder=os.path.join(basedir, 'database'))

    def __init__(self, parent, name='test', configfile=(), *args, **kwargs):
        """
        parent    : parent Tkinter class
        name      : Name of the tab, must be unique as it's used to switch to the tab
        configfile: Tuple of (filename, subroot tag)
        -----------------------------------------------------------------------------
        Tab is the base class for any Application, tab management code is located in
        ../tkroopy.py

        - Initiates a database connection
        - Defines class variables from application config file
        - Creates a vertical scroll bar for the application
        """
        Tkinter.Frame.__init__(self, parent, bd=2, relief="sunken", *args, **kwargs)
        self.name = name
        self.configfile = configfile
        self.parent = parent
        self.basedir = basedir
        self.title = None
        log.debug("# %s Application Initiated" % self.name)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Tkinter.Scrollbar(self, orient=Tkinter.VERTICAL)
        vscrollbar.pack(side="right", fill="y",  expand="false")
        self.canvas = Tkinter.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set, **kwargs)
        self.canvas.pack(side="left", fill="both", expand="true")
        vscrollbar.config(command=self.canvas.yview)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Tkinter.Frame(self.canvas, padx=5, pady=5, *args, **kwargs)
        self.interior.pack(fill="both", expand="true")

        interior_id = self.canvas.create_window(0, 0, window=interior, anchor="nw")

        self.bind('<Configure>', self.set_scrollregion)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                self.canvas.config(width=self.interior.winfo_reqwidth())
        self.interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
        self.canvas.bind('<Configure>', _configure_canvas)

    def load(self):
        try:
            self.parent.status.write('%s loaded' % self.title)
        except AttributeError:
            pass

        # Check if a config filename as passed tuple of (filename, subroot tag)
        # configfile is used in cases where an application has a super class where we want to initiate the super class config file not the subclass
        xml_name = ''
        if self.configfile:
            configfile, xml_name = self.configfile
        else:
            configfile = self.name.split('.')[-1].replace(" ", "_").lower()
            xml_name = self.name.split('.')[-1].replace(" ", "_").lower()

        # Load config for page
        try:
            import xml.etree.ElementTree as ET
            #import inspect
            log.debug('------------------------------------------------')
            log.debug(r'%s\config\%s.xml - %s' % (basedir, configfile, xml_name))

            with open(r'%s\config\%s.xml' % (basedir, configfile), 'rt') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                # Create class variables from the config xml file
                for child in root.find(xml_name):
                    if child.attrib:
                        # tags in the root with attributes will create instance variable data type value
                        # e.g. <temp_dir value='C:\Users\simpsonh\Documents\Projects\Temp' />
                        # will result in self.temp_dir = r'C:\Users\simpsonh\Documents\Projects\Temp'
                        log.debug('%s: %s' %(child.tag, child.attrib))
                        setattr(self, child.tag, child.attrib['value']) # self -> Page
                    else:
                        # tags in the root with no attributes will create instance variables of ElementTree objects
                        # e.g. <test_scripts><email>...</email></test_scripts>
                        # will result in self.test_scripts = <Element 'test_scripts' at 0x2c5c730>
                        # which can be further query the element using e.g. self.test_scripts.find('email/recipient')
                        log.debug('%s: %s' %(child.tag, child))
                        setattr(self, child.tag, child) # self -> Page
        except IOError as e:
            log.debug(e)

    def _on_mousewheel(self, event):
        #test = -1*(event.delta/120)
        self.canvas.yview_scroll(-1*(event.delta/120), "units")

    def set_scrollregion(self, event=None):
        """ Set the scroll region on the canvas"""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))



if __name__ == '__main__':
    root = Tkinter.Tk()
    main = Page(root, 'test')
    main.pack()
    for x in range(20):
        Tkinter.Checkbutton(main.interior, text="hello world! %s" % x).grid(row=x, column=0)
    root.mainloop()
