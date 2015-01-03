# -*- coding: utf-8 -*-#
import Tkinter
import logging
import sys, os

# set basedir for testing this application
if '__file__' in globals():
    basedir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..')
    sys.path.append(basedir)

    format = '%(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s'
    logging.basicConfig(format=format, level=logging.NOTSET)

import src.modules.page as page
import src.modules.table as table
from contrib.pydal import DAL, Field

db = page.Page.db
log = logging.getLogger(__package__)

class Movie_Db(page.Page):
    """
    Movie Db - An example of how a table works
    """
    production = False

    def __init__(self, root, name, *args, **kwargs): #, basedir

        page.Page.__init__(self, root, name) #, basedir

        # Displayed in the main menu
        self.title = 'Movie Database'
        self.image_path = 'movie_db.gif'
        # Define database tables.
        self.models()


    @staticmethod
    def models():
        """
        Define our tables, create instances of our tables in DAL
        Documentation on DAL:
        http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer
        """

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

        ## self.interior is the frame which sits inside the canvas to enable vertical scrolling
        self.frame_main = Tkinter.Frame(self.interior)
        self.frame_main.pack()

        # Any code here will be run when the application is initialised i.e. clicked on.
        data = db(db.movie.id>0).select()

        # Add record
        def add_record():
            frame_movie = Add_Record(self.root, 'examples.movie_db.Add_Record') #, self.basedir
            frame_movie.pack(expand="true", fill="both")

            self.root.add_page(frame_movie, None)
            self.root.change_page('examples.movie_db.Add_Record')

        btn_add = Tkinter.Button(self.frame_main, text='Add Record', command=add_record)
        btn_add.pack(anchor='w')

        def remove_record(id):
            db(db.movie.id==id).delete()
            db.commit()
            self.load()

        def edit_record(record_id):
            log.debug(record_id)
            frame_movie = Add_Record(self.root, 'examples.movie_db.Add_Record', record_id) #, self.basedir
            frame_movie.pack(expand="true", fill="both")

            self.root.add_page(frame_movie, None)
            self.root.change_page('examples.movie_db.Add_Record')

        # display the data in a table/grid view
        buttons = [dict(text='Edit', function=lambda row: edit_record(row['id'])), dict(text='Delete', function=lambda row: remove_record(row['id']))]
        grid_top_ten = table.Table(self.frame_main, data=data, buttons=buttons)
        grid_top_ten.pack()


class Add_Record(page.Page):
    """
    Creates a new tab to allow the use to create/edit the movie record
    """
    def __init__(self, root, name, record_id=None, *args, **kwargs): #, basedir

        page.Page.__init__(self, root, name) #, basedir

        self.record_id = record_id

    def load(self):
        """
        When the Add Record or Edit button is clicked in Movie_Db this page will be loaded
        """
        # Remove any previous instances of application UI
        try:
            self.frame_main.pack_forget()
            self.frame_main.destroy()
        except:
            pass

        self.frame_main = Tkinter.Frame(self.interior)
        self.frame_main.pack()

        # If record_id was passed (edit) get the record from db
        record = db.movie(self.record_id) or None

        # Form
        form_widgets = dict()
        for i, field in enumerate(db.movie):

            if field.type in ('string', 'float', 'integer'):
                # Any of the above data types will be captured in an Entry widget
                Tkinter.Label(self.frame_main, text=field.name.title()).grid(column=0, row=i)
                form_widgets[field.name] = Tkinter.Entry(self.frame_main)
                form_widgets[field.name].grid(column=1, row=i)
                try:
                    # if we are editting a record, insert the data into the Entry widget
                    form_widgets[field.name].insert('end', record[field.name])
                except TypeError:
                    pass
            elif field.type == 'id':
                # don't display the Id field
                pass

        def save_record():
            record = dict()
            for k, v in form_widgets.iteritems():
                record[k] = v.get()

            log.debug(record)
            db.movie.update_or_insert(db.movie.id==self.record_id, **record)
            db.commit()

            # change back to the Movie_Db page
            self.root.change_page('examples.Movie_Db')

        Tkinter.Button(self.frame_main, text='Save', command=save_record).grid(column=0, row=i+1)


if __name__ == '__main__':
    import importlib

    root = Tkinter.Tk()
    main = Movie_Db(root, "examples.Movie_Db")
    main.load()
    main.pack(expand="true", fill="both")
    root.mainloop()
    exit()


# ------ END OF FILE ----