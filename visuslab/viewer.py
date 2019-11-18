from OpenVisus import *

class ViewerNode(Node):
    def __init__(self, name="viewer node"):
        super().__init__(name)
        self.addInputPort("data")
        self.addInputPort('dataset')

    def getOsDependentTypeName(self):
        return "ViewerNode"

    def processInput(self):
        print("processInput")
        return super().processInput()

