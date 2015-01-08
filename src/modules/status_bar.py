import Tkinter
import Queue

class Status_Bar(Tkinter.Frame):
    def __init__(self, master, **options):
        Tkinter.Frame.__init__(self, master)

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
                    #self.v_status.set(status)
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
