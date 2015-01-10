#-------------------------------------------------------------------------------
# Name:        Table
# Purpose:     Tabularise data
#
# Author:      James Burke
# Created:     8/09/2014
#
# Copyright:   (c) James Burke 2014
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
import Tkinter
from functools import partial
import logging
from contrib.pydal import DAL

format = '%(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s'
logging.basicConfig(format=format, level=logging.NOTSET)

log = logging.getLogger(__package__)

class Table(Tkinter.Frame):

    def __init__(self, parent, data, header=True, links=[], buttons=[], pagination=0, **kwargs):
        """
        header: bool - first row header names
        data: list of list - data to display
        links: list of dict - (header=header label, body=lambda expression)
            Note: the difference between a link and a button, a link can be anything a button is a button.
        buttons: list of dict - (header=button label, function=lambda expression)
        pagination: integer - number of rows for each page
        """
        Tkinter.Frame.__init__(self, parent, **kwargs)

        self.parent = parent
        self.data = data
        self.header = header
        self.links = links
        self.buttons = buttons
        self.pagination = pagination

        if self.pagination:
            self.page_change(1)
        else:
            self.load_table(data)


    def load_table(self, data):
        """
        Load data into table
        """

        # Reload frame
        try:
            self.frame_table.pack_forget()
            self.frame_table.destroy()
        except:
            pass
        self.frame_table = Tkinter.Frame(self)
        self.frame_table.pack(side='top')

        header_i = 0

        log.debug(data)
        if str(type(data)) == '<class \'contrib.pydal.objects.Rows\'>':
            for header in data.colnames:
                header = header.split('.')[1].title()
                Tkinter.Label(self.frame_table, text=header, bg="grey").grid(row=0, column=header_i, padx=1, pady=1, sticky='nsew')
                header_i += 1
        elif isinstance(data, list) and isinstance(data[0], list):
            for header in self.data[0]:
                Tkinter.Label(self.frame_table, text=header, bg="grey").grid(row=0, column=header_i, padx=1, pady=1, sticky='nsew')
                header_i += 1
        else:
            raise TypeError('Must be type [Dict()] or DAL select result got %s' %(type(data)))

        for link in self.links:
            Tkinter.Label(self.frame_table, text=link['header'], bg="grey").grid(row=0, column=header_i, padx=1, pady=1, sticky='nsew')
            header_i += 1
        if self.buttons:
            Tkinter.Label(self.frame_table, text="", bg="grey").grid(row=0, column=header_i, padx=1, pady=1, sticky='nsew')

        # row and column positions in the grid.
        col_i = 1
        row_i = 1

        for row in data:

            if str(type(data)) == '<class \'contrib.pydal.objects.Rows\'>':
                for col_i, col in enumerate(data.colnames):
                    row_item = Tkinter.Label(self.frame_table, text=row[col])
                    row_item.grid(row=row_i, column=col_i, padx=1, pady=1, sticky='w')
                col_i += 1
            elif isinstance(data, list) and isinstance(data[0], list):
                if row == data[0] and self.header:
                    # don't output the first row if it's expected to be the header
                    continue
                col_i = 0
                for col in row:
                    row_item = Tkinter.Label(self.frame_table, text=col)
                    row_item.grid(row=row_i, column=col_i, padx=1, pady=1, sticky='w')
                    col_i += 1


            for link in self.links:
                row_item = link['body'](self.frame_table, row)
                row_item.grid(row=row_i, column=col_i, padx=1, pady=1, sticky='w')

                col_i += 1

            if self.buttons:
                frame_btns = Tkinter.Frame(self.frame_table)
                frame_btns.grid(row=row_i, column=col_i)
                btn_i = 0
                if self.buttons:
                    for button in self.buttons:
                        try:
                            param = button['parameters']
                        except:
                            param = row
                        map_command = partial(button['function'], param)
                        btn_map = Tkinter.Button(frame_btns, text=button['text'], command=map_command)
                        btn_map.grid(row=0, column=btn_i, padx=1, pady=1, sticky='w')
                        btn_i += 1
                col_i += 1
            row_i += 1

    def load_page(self, selected_page):
        if self.pagination:
            import math
            try:
                self.frame_page.pack_forget()
                self.frame_page.destroy()
            except:
                pass

            self.frame_page = Tkinter.Frame(self)
            self.frame_page.pack(side='bottom', anchor='ne')
            pages = int(math.ceil(float(len(self.data)) / float(self.pagination))) + 1

            page_i = 0
            for page in range(1, pages):
                if page == selected_page:
                    btn_map = Tkinter.Button(self.frame_page, text=page, relief="sunken", command=lambda page=page:self.page_change(page))
                else:
                    btn_map = Tkinter.Button(self.frame_page, text=page, command=lambda page=page:self.page_change(page))
                btn_map.grid(row=0, column=page_i, padx=1, pady=1, sticky='w')
                page_i += 1

    def page_change(self, page):
        """
        Change to a page number
        """
        if page == 1:
            start = 0
            end = self.pagination
        elif page == 2:
            start = self.pagination
            end = self.pagination + self.pagination
        else:
            start = (page - 1) * self.pagination
            end = ((page - 1) * self.pagination) + self.pagination
        self.load_table(self.data[start:end]) # , page
        self.load_page(page)

    def show_record(self, record):
        """
        Change to the page with the speicified record
        """
        import math
        page = int(math.ceil(float(record) / float(self.pagination)))
        log.debug(page)
        self.page_change(page)

if __name__ == '__main__':
    def btn_click(p):
        print p

    import tab
    root = Tkinter.Tk()
    data = [['test', 'test1']]
    data += [['r%s_c1' % x,'r%s_c2' % x] for x in range(1,20)]

    links = [dict(header='Test', body=lambda root, row: Tkinter.Button(root, text='rolf', command=lambda : btn_click(row[1])))]
    buttons = [dict(text='test1', function=lambda row: btn_click(row[0])),
               dict(text='test2', function=btn_click, parameters=dict(hello='world'))]

    table = Table(root, header=True, data=data, links=links, buttons=buttons)
    table.pack()
    root.mainloop()