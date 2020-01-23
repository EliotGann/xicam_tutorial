from xicam.core.execution import Workflow
from xicam.plugins.operationplugin import OperationPlugin
from ..operations import fft, realpart, imagpart,absval, fft2

class MyWorkflow(Workflow):
    def __init__(self):
        super(MyWorkflow, self).__init__()

        # add_operation()
        # workflow.add_operation(mask_operation)
        # workflow.add_operation(fft_operation)

        # auto_connect_all()

        #workflow = Workflow()
        self.add_operation(fft)
        self.auto_connect_all()
