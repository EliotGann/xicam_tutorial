from xicam.plugins import GUIPlugin, GUILayout, OperationPlugin
from qtpy.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton
from databroker.core import BlueskyRun
from xicam.core.msg import notifyMessage
from xicam.gui.widgets.imageviewmixins import CatalogView, BetterButtons
from .workflows import MyWorkflow

# Create a "blend" class from 2 xicam image view mixings
class MyImageViewer(BetterButtons, CatalogView):
    def __init__(self,*args, **kwargs):
        super(MyImageViewer,self).__init__(*args,**kwargs)

class MyGUIPlugin(GUIPlugin):
    name = "My Plugin"

    def __init__(self):
        #Define workflows
        self.my_workflow = MyWorkflow()

        # Define a GUILayout
        # GUILayouts must provide a center widget
        self.center_widget = QWidget()
        layout = QVBoxLayout() # what kind of layout
        self.catalog_view = CatalogView()
        self.label = QLabel('2')
        self.button = QPushButton("push this")
        layout.addWidget(self.catalog_view) # add things to the layout one by one
       # layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.center_widget.setLayout(layout) # apply layout to the basic widget
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
        #self.button.clicked.connect(self.update_label)
        self.button.clicked.connect(self.show_message)
        self.button.clicked.connect(self.run_workflow)
        self.stages = {'first_stage': stage_layout}

        super(MyGUIPlugin, self).__init__()

    def appendCatalog(self, catalog:BlueskyRun):
        # give catalog to out catalog viewer
        self.catalog_view.setCatalog(catalog,'primary','img')

    def update_label(self):
        current_text = self.label.text()
        current_text += "1"
        self.label.setText(current_text)

    def show_message(self):
        notifyMessage("Add another 1.")

    def show_message(self, catalog:BlueskyRun):
        notifyMessage(f'Added catalog {catalog}')

    def run_workflow(self):
        # workflow has an exec() and an exec_all() to run itself
        # extract data from loaded catalog
        if not self.catalog_view.catalog:
            notifyMessage("A catalog is not yet loaded, please load one first")
            return
        image_data = self.catalog_view.catalog.primary.to_dask()['img'].compute()
        # primary.image.read()
        # execute wkll take in named inputs in your OperationPlugin,
        # and a callback_slot will be called when it finished execution
        self.my_workflow.execute(input_image=image_data,
                                 callback_slot=self.show_fft)

    def show_fft(self,*results): # workflow results have a *results passed into them
        # results : a list of dictionarys result objects, eg [ {"output_image":
        #from qtpy.QtCore import pyqtRemoveInputHook
        #pyqtRemoveInputHook()
        #import pdb
        #pdb.set_trace()
        #print(results)
        fft_image = results[-1]['output_image']
        import matplotlib.pyplot as plt
        plt.imshow(fft_image[0])
        plt.show()