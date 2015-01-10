#-------------------------------------------------------------------------------
# Name:        Status Bar
# Purpose:     Threadsafe status bar update
#
# Author:      James Burke
# Created:     8/01/2015
#
# Copyright:   (c) James Burke 2015
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
import Queue

class Status_Bar(Tkinter.Frame):
    def __init__(self, master, **kwargs):
        Tkinter.Frame.__init__(self, master, **kwargs)

        # Status
        self.v_status = Tkinter.StringVar()
        self.v_status.set('Status')

        # Label
        label_status = Tkinter.Label(self, textvariable=self.v_status)
        label_status.pack()

        self.queue = Queue.Queue()
        self.update_me()
    def write(self, status):
        self.queue.put(status)
    def clear(self):
        self.queue.put(None)
    def update_me(self):
        try:
            while 1:
                status = self.queue.get_nowait()

                if status is None:
                    self.v_status.set('Status')
                else:
                    try:
                        self.after_cancel(self.after_id)
                    except AttributeError:
                        pass
                    self.v_status.set('Status: %s' % status)
                    self.after_id = self.after(2000, self.clear)
                self.update_idletasks()
        except Queue.Empty:
            pass
        self.after(100, self.update_me)
