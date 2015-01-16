# -*- coding: utf-8 -*-#
import Tkinter
import logging
import glob, os
import importlib
import zipfile

if '__file__' in globals():
    basedir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')

try:
    import src.modules.page as page
except:
    import sys
    sys.path.append(r'%s\src' % basedir)
    import modules.page as page
    import modules.table as table

    format = '%(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s'
    logging.basicConfig(format=format, level=logging.NOTSET)

log = logging.getLogger(__package__)
log.debug(basedir)

class Main(page.Page):
    """
    Main menu for tKroopy applications
    """
    def __init__(self, root, name, *args, **kwargs):
        """
        root    : root Tkinter class
        name      : Name of the page, must be unique as it's used to switch to the page
        basedir   : Application root directory
        -----------------------------------------------------------------------
        Initiates all of the applications and provides buttons/icons for each of
        the applications allowing the user to click on them to launch the application.

        Applications are stored in a hierarchical structure in the Applications directory.
        """
        page.Page.__init__(self, root, name, *args, **kwargs)

        # Page controll or window control
        self.title = 'Main Menu'

        myzip = r'library.zip'

        try:
            # Folder location
            application_folder = os.path.join(self.basedir, 'src/applications')
            application_subfolders = [d for d in os.listdir(application_folder) if os.path.isdir(os.path.join(application_folder, d)) ]
            application_subfolders.append('')
            log.debug("Categories: %s" % application_subfolders)

        except OSError as e:
            log.debug(e)
            with zipfile.ZipFile(myzip) as z:
                application_subfolders = [x for x in z.namelist() if r'src/applications' in x]

                log.debug("Modules: %s" % application_subfolders)
                application_subfolders = [ os.path.dirname(f).split('/')[-1] for f in application_subfolders]# if os.path.basename(f) not in ['main.pyc', '__init__.pyc','main.py', '__init__.py', 'template.py', 'template.pyc']]
                application_subfolders = set(application_subfolders)
                application_subfolders = list(application_subfolders)
                log.debug("Modules: %s" % application_subfolders)

        for folder in application_subfolders:
            # Create category frame
            frame_category = Tkinter.LabelFrame(self.interior, text=folder.title(), border="0", bg="white")
            frame_category.pack(expand="true", fill="both", padx="5")

            # Dynamically import all of the modules in src.applications
            modules = glob.glob(os.path.join(application_folder, folder)+"/*.py")
            log.debug("Modules: %s" % modules)

            # the previous statement doesn't work in the compiled code
            if not modules:
                with zipfile.ZipFile(myzip) as z:
                    # get the modules from library.zip
                    modules = [x for x in z.namelist() if r'src/applications/%s' % folder in x]

            # filter out any modules that we don't want showing up in the main menu
            log.debug("Modules: %s" % modules)
            modules = [ os.path.basename(f).split('.')[0] for f in modules if os.path.basename(f).split('.')[0] not in ['__init__', 'template', 'main']]
            log.debug("Modules: %s" % modules)

            #else:
            #    log.debug("Modules: %s" % modules)
            #    log.debug(glob.glob(os.path.join(application_folder, folder)+"/_*.py"))
            #    modules = [ os.path.basename(f)[:-3] for f in modules if os.path.basename(f) not in ['__init__.py', 'template.py']]
            #    log.debug("Modules: %s" % modules)

            row_num = 0
            col_num = 0
            for module_name in modules:
                name = module_name.replace("_", " ").title()
                class_name = name.replace(" ", "_")
                log.debug('src.applications.%s.%s' % (folder, module_name))
                try:
                    module = importlib.import_module('src.applications.%s.%s' % (folder, module_name))
                except ValueError:
                    module = importlib.import_module('src.applications.%s' % (module_name))

                app = getattr(module, class_name)

                # Check if the App has been productionised or running development version
                log.debug(root.production)
                if app.production or bool(root.production):
                    # Create a frame for the app/module
                    frame_app = app(root, name='%s.%s' % (folder, class_name), bd=2, relief="sunken")
                    frame_app.pack(side='top', expand="true", fill="both")

                    log.debug("Frameapp Name: %s" % frame_app.name)

                    # Create a button for the app/module
                    def load_app(frame_app):
                        """
                        Call Back: switches page to the application frame and loads the application
                        """
                        root.change_page(frame_app.name)
                        #frame_app.load()


                    # set the Application icon image
                    try:
                        frame_app.image = Tkinter.PhotoImage(file=os.path.join(self.basedir, 'images/%s' %frame_app.image_path))
                    except AttributeError:
                        frame_app.image = Tkinter.PhotoImage(file=os.path.join(self.basedir, 'images/placeholder.gif'))
                    except Exception as e:
                        log.error(e)
                    btn_app = Tkinter.Button(frame_category, text=frame_app.title, image=frame_app.image, compound="top", relief="flat", bg="white", activebackground="white", command=(lambda frame_app=frame_app: load_app(frame_app)))
                    btn_app.grid(row=row_num, column=col_num, padx=10, pady=10)

                    # Create a new page
                    root.add_page(frame_app, btn_app)

                    # Positioning of buttons
                    # 8 per row
                    if col_num >= 8:
                        col_num = 0
                        row_num += 1
                    else:
                        col_num += 1

    def load(self):
        pass


if __name__ == '__main__':
    root = Tkinter.Tk()
    main = Main(root, "Main")
    main.pack()
    root.mainloop()


# ------ END OF FILE ----
