#-------------------------------------------------------------------------------
# Name:        Search
# Purpose:     Create an Entry widget with a dropdown of search results
# Source:      http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/
#
# Author:      Miguel Angel Alarcos Torrecillas
# Created:     6/09/2012
# Modified:    9/01/2015 jburke
#
# Copyright    (c) Miguel Angel Alarcos Torrecillas 2012
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
from Tkinter import *
import re
import logging
from contrib.pydal import DAL, Field

log = logging.getLogger(__package__)
db2 = None

class Search(Entry):
    def __init__(self, root, db, queries=(), command=None, **kwargs):

        Entry.__init__(self, root, **kwargs)
        self.db = db
        self.root = root
        self.queries = queries

        log.debug(self.winfo_reqwidth())
        self.result = StringVar()
        self.result.trace('w', command)

        self.selected = None

        self.var = self["textvariable"]

        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        self.lb_up = False

    def changed(self, name, index, mode):
        def callback():
            if self.var.get() == '' or len(self.var.get()) < 3 or self.var.get() == self.selected:
                try:
                    self.lb.destroy()
                except AttributeError:
                    pass
                self.lb_up = False

            else:
                results = self.comparison()
                if results:
                    if not self.lb_up:
                        self.lb = Listbox(width=int(float(self.winfo_reqwidth())*0.165)) #
                        self.lb.bind("<Double-Button-1>", self.selection)
                        self.lb.bind("<Right>", self.selection)
                        #relx=0.5, y=self.winfo_y()+self.winfo_height()+5
                        self.lb.place(in_=self.root, x=self.winfo_x()-3, y=self.winfo_y()+3) #relx=0.5, x=-215,

                        self.lb_up = True
                    self.results = results
                    self.lb.delete(0, END)

                    for w in results:
                        try:
                            self.lb.insert(END,w[1])
                        except AttributeError:
                            self.lb.insert(END, w)

                else:
                    if self.lb_up:
                        self.lb.destroy()
                        self.lb_up = False
        try:
            self.after_cancel(self.after_id)
        except AttributeError:
            pass
        self.after_id = self.after(1000, callback)

    def selection(self, event):

        if self.lb_up:

            self.var.set(self.lb.get(ACTIVE))
            try:
                self.result.set([item[0] for item in self.results if int(self.var.get()) in item][0])
            except ValueError as e:
                self.result.set([item[0] for item in self.results if self.var.get() in item][0])
                #log.error(e)
                #log.debug(type(self.var.get()))

            self.selected = self.var.get()
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)
            #log.debug(self.var.get())
            #log.debug(self.words)
            #for item in self.words:
            #    log.debug(item)
            #    if int(self.var.get()) in item:
            #        log.debug(item)


    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        db = self.db
        results = []
        log.debug(self.queries)
        for query, fields in self.queries:
            # convert rows into lists of values [[1, 'Clerks.']] etc
            results += [item.values() for item in db(query.contains(self.var.get())).select(*fields).as_list()]
        log.debug(results)
        return results


if __name__ == '__main__':
    # No example yet!
    root = Tk()
    root.mainloop()
