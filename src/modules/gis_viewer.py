#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      James
#
# Created:     14/01/2015
# Copyright:   (c) James 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import Tkinter
import urllib, cStringIO
from PIL import Image, ImageTk

class GIS_Viewer(Tkinter.Canvas):

    def __init__(self, *args, **kwargs):
        Tkinter.Canvas.__init__(self, *args, **kwargs)

        url = "http://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/13/3099/1698.png"
        file = cStringIO.StringIO(urllib.urlopen(url).read())
        pic = Image.open(file)
        image = ImageTk.PhotoImage(pic)
        self.create_image(image=image)

        #label = Tkinter.Label(image=image)
        #label.image = image
        #label.pack()

if __name__ == '__main__':
    root = Tkinter.Tk()
    gis_viewer = GIS_Viewer(root)
    gis_viewer.pack()

    root.mainloop()
    exit()
