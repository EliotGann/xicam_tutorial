from xicam.plugins import GUIPlugin, GUILayout
#from qtpy.QtGui import
from qtpy.QtWidgets import QLabel
from databroker.core import BlueskyRun
from xicam.gui.widgets.imageviewmixins import CatalogView, BetterButtons


# Create a "blend" class from 2 xicam image view mixings
class MyImageViewer(BetterButtons, CatalogView):
    def __init__(self,*args, **kwargs):
        super(MyImageViewer,self).__init__(*args,**kwargs)

class MyGUIPlugin(GUIPlugin):
    name = "My Plugin"

    def __init__(self):
        # Define a GUILayout
        # GUILayouts must provide a center widget
        self.center_widget = CatalogView()
        bottom_widget = QLabel('bottom')
        left_widget = QLabel('left')
        leftbottom_widget = QLabel('left bottom')
        right_widget = QLabel('right')
        stage_layout = GUILayout(center=self.center_widget,
                                 #left=left_widget,
                                 #right=right_widget,
                                 #leftbottom = leftbottom_widget,
                                 #bottom = bottom_widget,
                                 )

        self.stages = {'first_stage': stage_layout}

        super(MyGUIPlugin, self).__init__()

    def appendCatalog(self, catalog:BlueskyRun):
        # give catalog to out catalog viewer
        self.center_widget.setCatalog(catalog,'primary','img')