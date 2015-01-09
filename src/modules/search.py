from Tkinter import *
import re
import logging

log = logging.getLogger(__package__)

import src.modules.dal as dal

class Search(Entry):
    def __init__(self, root, db, queries, command, *args, **kwargs):

        Entry.__init__(self, root, *args, **kwargs)
        self.db = db
        self.queries = queries

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
                        self.lb = Listbox(width=60)
                        self.lb.bind("<Double-Button-1>", self.selection)
                        self.lb.bind("<Right>", self.selection)
                        self.lb.place(relx=0.5, x=-215, y=self.winfo_y()+self.winfo_height()+5)

                        self.lb_up = True
                    self.results = results
                    self.lb.delete(0, END)

                    for w in results:
                        self.lb.insert(END,w[1])

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
        results = []
        for query in self.queries:
            results += self.db.select(query.replace('[search]',self.var.get().replace(' ', '')))
        return results # self.words =


if __name__ == '__main__':
    root = Tk()

    lista = ['test', 'test1', 'test2', 'test3']
    entry = Search(lista, root)
    entry.grid(row=0, column=0)
    Button(text='nothing').grid(row=1, column=0)
    Button(text='nothing').grid(row=2, column=0)
    Button(text='nothing').grid(row=3, column=0)

    root.mainloop()
