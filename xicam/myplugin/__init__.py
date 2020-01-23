
from qtpy.QtCore import Signal, Qt, QItemSelectionModel
from qtpy.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QSplitter
from qtpy.QtGui import QStandardItem, QStandardItemModel
from pyqtgraph.parametertree import ParameterTree, Parameter
from pyqtgraph.parametertree.parameterTypes import ListParameter

from databroker.core import BlueskyRun
from xicam.core.msg import notifyMessage
from xicam.gui.widgets.imageviewmixins import CatalogView, BetterButtons, ImageView
from xicam.gui.widgets.linearworkfloweditor import WorkflowEditor
from xicam.gui.widgets.tabview import TabView
from xicam.plugins import GUIPlugin, GUILayout, OperationPlugin

from .workflows import MyWorkflow

# Create a "blend" class from 2 xicam image view mixings
class MyImageView(BetterButtons, CatalogView):
    def __init__(self,*args, **kwargs):
        super(MyImageView,self).__init__(*args,**kwargs)


# Widget that shows both our catalog image view and the results image view
class CatalogAndAnalysisSplitWidget(QWidget):
    def __init__(self,*args):
        super(CatalogAndAnalysisSplitWidget, self).__init__(*args)

        self.splitter = QSplitter(Qt.Horizontal)
        self.catalog_view = MyImageView()
        self.results_view = ImageView()
        self.splitter.addWidget(self.catalog_view)
        self.splitter.addWidget(self.results_view)
        layout = QVBoxLayout()
        layout.addWidget(self.splitter)
        self.setLayout(layout)

    def set_image(self,image):
        self.results_view.setImage(image)

    def catalog(self):
        return self.catalog_view.catalog


class MyGUIPlugin(GUIPlugin):
    name = "My Plugin"

    def __init__(self):
        #Define workflows
        self.my_workflow = MyWorkflow()
        #self.my_workflow_editor = WorkflowEditor(self.my_workflow)
        # Define a GUILayout
        # GUILayouts must provide a center widget
        #self.container_widget = QWidget()
        self.split_widget = CatalogAndAnalysisSplitWidget()
        layout = QVBoxLayout() # what kind of layout
        self.button = QPushButton("push this")
        #layout.addWidget(self.split_widget) # add things to the layout one by one
        #layout.addWidget(self.button)
        #self.container_widget.setLayout(layout) # apply layout to the basic widget
        bottom_widget = QLabel('bottom')
        left_widget = QLabel('left')
        leftbottom_widget = QLabel('left bottom')
        right_widget = QLabel('right')

        self.model = QStandardItemModel()
        self.selectionmodel = QItemSelectionModel(self.model)
        stream = 'primary'
        field = 'img'
        self.test_tab_view = TabView(self.model,self.selectionmodel,widgetcls=MyImageView,stream=stream,field=field)


        self.parameter_view = ParameterTree()
        for operation in self.my_workflow.operations:
            parameter_dict = operation.as_parameter()
            for list_parameter in parameter_dict:
                parameter = Parameter.create(**list_parameter)
                self.parameter_view.addParameters(parameter)
        stage_layout = GUILayout(center=self.split_widget,
                                 #left=left_widget,
                                 #right=right_widget,
                                 #leftbottom = leftbottom_widget,
                                 bottom = self.button,
                                 )
        second_stage_layout = GUILayout(center=self.test_tab_view, righttop=self.parameter_view)
        #workflow_stage = GUILayout(center=self.test_tab_view, righttop=self.my_workflow_editor)
        #self.button.clicked.connect(self.update_label)
        #self.button.clicked.connect(self.show_message)
        self.button.clicked.connect(self.run_workflow)
        self.stages = {'catalogviewer and fft': stage_layout,
                       'Something Else': second_stage_layout,
                       #'testing workflow editor': workflow_stage,
                       }

        super(MyGUIPlugin, self).__init__()

    def appendCatalog(self, catalog:BlueskyRun):
        # give catalog to out catalog viewer
        self.split_widget.catalog_view.setCatalog(catalog, 'primary', 'img')

        display_name = f"scan:{catalog.metadata['start']['scan_id']}"
        item = QStandardItem()
        item.setData(display_name,Qt.DisplayRole)
        item.setData(catalog, Qt.UserRole)
        self.model.appendRow(item)
        # tell our model that the data has been updated, the two parameters are rox index and column index
        self.model.dataChanged.emit(item.index(), item.index())


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
        if not self.split_widget.catalog_view.catalog:
            notifyMessage("A catalog is not yet loaded, please load one first")
            return
        image_data = self.split_widget.catalog_view.catalog.primary.to_dask()['img'].compute()
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
        self.split_widget.results_view.setImage(fft_image)
        #import matplotlib.pyplot as plt
        #plt.imshow(fft_image[0])
        #plt.show()