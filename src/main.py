# -*- coding: utf-8 -*-#
import Tkinter
import logging
import glob, os
import importlib
import zipfile

if '__file__' in globals():
    basedir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

try:
    import src.modules.tab as tab
except:
    import sys
    sys.path.append(r'%s\src' % basedir)
    import modules.tab as tab
    import modules.table as table

    format = '%(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s'
    logging.basicConfig(format=format, level=logging.NOTSET)

log = logging.getLogger(__package__)
log.debug(basedir)

class Main(tab.Tab):
    """
    Main menu for tKroopy applications
    """
    def __init__(self, root, name, basedir, *args, **kwargs):
        """
        root    : root Tkinter class
        name      : Name of the tab, must be unique as it's used to switch to the tab
        basedir   : Application root directory
        -----------------------------------------------------------------------
        Initiates all of the applications and provides buttons/icons for each of
        the applications allowing the user to click on them to launch the application.

        Applications are stored in a hierarchical structure in the Applications directory.
        """
        tab.Tab.__init__(self, root, name, basedir, *args, **kwargs)

        # Tab controll or window control
        self.title = 'Main Menu'

        myzip = r'library.zip'

        try:
            # Folder location
            application_folder = os.path.join(self.basedir, r'src\applications')
            application_subfolders = [d for d in os.listdir(application_folder) if os.path.isdir(os.path.join(application_folder, d))]
            application_subfolders.append('')
            log.debug("Categories: %s" % application_subfolders)
        except WindowsError as e:
            log.debug(e)
            with zipfile.ZipFile(myzip) as zipper:
                application_subfolders = [x for x in zipper.namelist() if r'src/applications' in x]

                log.debug("Modules: %s" % application_subfolders)
                application_subfolders = [ os.path.dirname(f).split('/')[-1] for f in application_subfolders if os.path.basename(f) not in ['main.pyc', '__init__.pyc','main.py', '__init__.py']]
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
                with zipfile.ZipFile(myzip) as zipper:
                    modules = [x for x in zipper.namelist() if r'src/applications/%s' % folder in x]

                    log.debug("Modules: %s" % modules)
                    modules = [ os.path.basename(f)[:-4] for f in modules if os.path.basename(f) not in ['main.pyc', '__init__.pyc']]
                    log.debug("Modules: %s" % modules)
            else:
                log.debug("Modules: %s" % modules)
                modules = [ os.path.basename(f)[:-3] for f in modules if os.path.basename(f) not in ['main.py', '__init__.py']]
                log.debug("Modules: %s" % modules)

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
                log.debug(self.root.production)
                if app.production or bool(self.root.production):
                    # Create a frame for the app/module
                    frame_app = app(self.root, name='%s.%s' % (folder, class_name), basedir=basedir, bd=2, relief="sunken")
                    frame_app.pack(expand="true", fill="both")

                    log.debug("Frameapp Name: %s" % frame_app.name)

                    # Create a button for the app/module
                    def load_app(frame_app):
                        """
                        Call Back: switches tab to the application frame and loads the application
                        """
                        self.root.switch_tab(frame_app.name)
                        #frame_app.load()


                    # set the Application icon image
                    try:
                        frame_app.image = Tkinter.PhotoImage(file=frame_app.image_path)
                    except AttributeError:
                        frame_app.image = Tkinter.PhotoImage(file=os.path.join(basedir, 'images/placeholder.gif'))
                    except Exception as e:
                        log.error(e)
                    btn_app = Tkinter.Button(frame_category, text=frame_app.title, image=frame_app.image, compound="top", relief="flat", bg="white", activebackground="white", command=(lambda frame_app=frame_app: load_app(frame_app)))
                    btn_app.grid(row=row_num, column=col_num, padx=10, pady=10)

                    # Add the button to the tab bar (home screen icons)
                    self.root.add(frame_app, btn_app)

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
    main = Main(root, "Main", basedir)
    main.pack()
    root.mainloop()


# ------ END OF FILE ----