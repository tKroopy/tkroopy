# -*- coding: utf-8 -*-#
import Tkinter
import logging
import sys, os
import webbrowser

# set basedir for testing this application
if '__file__' in globals():
    basedir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..')
    sys.path.append(basedir)

    format = '%(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s'
    logging.basicConfig(format=format, level=logging.NOTSET)

# import when running tkroopy
import src.modules.page as page
import src.modules.table as table
import src.modules.console as console
from contrib.pydal import DAL, Field

db = page.Page.db
log = logging.getLogger(__package__)

class Fibonacci_Numbers(page.Page):
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
        self.title = 'Fibonacci Numbers'
        self.image_path = 'fibonacci_numbers.gif'
        self.models()
        # Enter any instance variables here.


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
        self.console_fib = console.Console(self.frame_main, width=50, height=20)
        self.console_fib.pack()
        self.console_fib.write("This example uses fibonacci numbers to explain how the console widget is threadsafe and will not lock your application while outputting to it.\n\n")
        self.console_fib.write("For more information about Fibonacci Numbers visit this ")
        self.console_fib.write('link\n\n', self.console_fib.link.add(lambda : webbrowser.open_new('http://en.wikipedia.org/wiki/Fibonacci_number')))


        def start():
            import threading
            t = threading.Thread(target=self.fibonacci_numbers)
            t.daemon = True
            t.start()

        btn_start = Tkinter.Button(self.frame_main, text='Start', command=start)
        btn_start.pack(anchor='w')

    def fibonacci_numbers(self):
        import time

        def F():
            a,b = 0,1
            yield a
            yield b
            while True:
                a, b = b, a + b
                yield b

        def SubFib(startNumber, endNumber):
            for cur in F():
                if cur > endNumber: return
                if cur >= startNumber:
                    yield cur

        # clear text from console
        self.console_fib.clear()

        self.console_fib.write("This example uses fibonacci numbers to explain how the console widget is threadsafe and will not lock your application while outputting to it.\n\n")
        self.console_fib.write("For more information about Fibonacci Numbers visit this ")
        self.console_fib.write('link\n\n', self.console_fib.link.add(lambda : webbrowser.open_new('http://en.wikipedia.org/wiki/Fibonacci_number')))

        # output fibonnaci numbers to console
        for i in SubFib(0, 100):
            time.sleep(0.5)
            self.console_fib.write('%s\n' % i)
        self.console_fib.write('Done!')



if __name__ == '__main__':
    root = Tkinter.Tk()
    main = Fibonacci_Numbers(root, "Run Task")
    main.load()
    main.pack(expand="true", fill="both")
    root.mainloop()
    exit()


# ------ END OF FILE ----