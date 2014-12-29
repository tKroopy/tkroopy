# -*- coding: utf-8 -*-#
import Tkinter
import logging
import webbrowser
from functools import partial
import sys, os
from pydal import DAL, Field

# set basedir for testing this application
if '__file__' in globals():
    basedir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..')

try:
    # import when running tkroopy
    import src.modules.tab as tab
    import src.modules.grid as grid
except:
    # import when testing this application
    sys.path.append(r'%s\src' % basedir)
    import modules.tab as tab
    import modules.grid as grid
    format = '%(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s'
    logging.basicConfig(format=format, level=logging.NOTSET)

db = tab.Tab.db
log = logging.getLogger(__package__)

class Movie_Db(tab.Tab):
    """
    Table 1 - A simple example of how a grid works
    """
    production = False

    def __init__(self, root, name, basedir, *args, **kwargs):

        tab.Tab.__init__(self, root, name, basedir)

        # Displayed in the main menu
        self.title = 'Movie Database'
        self.models() # define database tables.

        # Enter any instance variables here
        ## self.interior is the frame which sits inside the canvas to enable vertical scrolling
        ## you could reference this directly but it's good to have a visable frame in your class


    @staticmethod
    def models():
        # Documentation on DAL
        # http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer

        # Define tables in database
        ## Movie
        db.define_table('movie',
            Field('title', required=True),
            Field('genre', required=True),
            Field('director', required=True),
            Field('rating', type='float', required=True),
            Field('year', type='integer', required=True),
            )


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

        self.frame_main = Tkinter.Frame(self.interior)
        self.frame_main.pack()

        # Any code here will be run when the application is initialised i.e. clicked on.
        data = db(db.movie.id>0).select()

        # Add record
        def add_record():
            frame_movie = Add_Record(self.root, 'examples.movie_db.Add_Record', self.basedir)
            frame_movie.pack(expand="true", fill="both")

            self.root.add(frame_movie, None)
            self.root.switch_tab('examples.movie_db.Add_Record')

        btn_add = Tkinter.Button(self.frame_main, text='Add Record', command=add_record)
        btn_add.pack(anchor='w')

        def remove_record(id):
            db(db.movie.id==id).delete()
            db.commit()
            self.load()

        def edit_record(record_id):
            log.debug(record_id)
            frame_movie = Add_Record(self.root, 'examples.movie_db.Add_Record', self.basedir, record_id)
            frame_movie.pack(expand="true", fill="both")

            self.root.add(frame_movie, None)
            self.root.switch_tab('examples.movie_db.Add_Record')

        # display the data in a table/grid view
        buttons = [dict(text='Edit', function=lambda row: edit_record(row['id'])), dict(text='Delete', function=lambda row: remove_record(row['id']))]
        grid_top_ten = grid.Grid(self.frame_main, data=data, buttons=buttons)
        grid_top_ten.pack()


class Add_Record(tab.Tab):

    def __init__(self, root, name, basedir, record_id=None, *args, **kwargs):

        tab.Tab.__init__(self, root, name, basedir)

        self.frame_main = Tkinter.Frame(self.interior)
        self.frame_main.pack()


        record = db.movie(record_id) or None

        # Form
        form_widgets = dict()
        for i, field in enumerate(db.movie):

            if field.type in ('string', 'float', 'integer'):
                Tkinter.Label(self.frame_main, text=field.name.title()).grid(column=0, row=i)
                form_widgets[field.name] = Tkinter.Entry(self.frame_main)
                form_widgets[field.name].grid(column=1, row=i)
                try:
                    form_widgets[field.name].insert('end', record[field.name])
                except TypeError:
                    pass
            elif field.type == 'id':
                pass

            log.debug(field.type)

        def save_record():
            log.debug(form_widgets)
            record = dict()
            for k, v in form_widgets.iteritems():
                record[k] = v.get()

            log.debug(record)
            db.movie.update_or_insert(db.movie.id==record_id, **record)
            db.commit()
            self.root.switch_tab('examples.Movie_Db')

        Tkinter.Button(self.frame_main, text='Save', command=save_record).grid(column=0, row=i+1)




    def load(self):
        # Must include a load method in your applications
        pass


if __name__ == '__main__':
    # testing application
    root = Tkinter.Tk()
    main = Movie_Db(root, "examples.Movie_Db", basedir)
    main.load()
    main.pack(expand="true", fill="both")
    root.mainloop()
    exit()


# ------ END OF FILE ----