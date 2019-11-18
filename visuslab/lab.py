from OpenVisus import *

from .viewer import ViewerNode


class VisusLab(DataflowListener):
# class VisusLab(object):
    def __init__(self):

        data = LoadDataset("http://atlantis.sci.utah.edu/mod_visus?dataset=david")

        self.field = None
        self.bounds = None
        self.dataflow = Dataflow()
        # self.dataflow.listeners.push_back(self)

        self.dataset_node = DatasetNode('Dataset node')
        self.dataflow.addNode(self.dataset_node)

        self.query_node = QueryNode('query node')
        self.dataflow.addNode(self.query_node)
        self.dataflow.connectPorts(self.dataset_node, "dataset", self.query_node)

        self.viewer_node = ViewerNode('viewer node')
        self.dataflow.addNode(self.viewer_node)
        self.dataflow.connectPorts(self.query_node, "data", self.viewer_node)
        self.dataflow.connectPorts(self.dataset_node, "dataset", self.viewer_node)

        self.dataset_node.setDataset(data, True)
        self.bounds = self.dataset_node.getNodeBounds()
        print("bounds:", self.bounds)

        self.query_node.setAccessIndex(0)
        self.query_node.setProgression(QueryGuessProgression)
        self.query_node.setViewDependentEnabled(True)
        self.query_node.setQuality(QueryDefaultQuality)
        self.query_node.setNodeBounds(self.bounds)
        self.query_node.setQueryBounds(self.bounds)


        self.set_time(data.getDefaultTime())
        self.set_field_name(data.getDefaultField().name)


    def set_field_name(self, name):
        self.query_node.getInputPort('fieldname').writeString(name)
        self.dataflow.needProcessInput(self.query_node)

    def set_time(self, value):
        port = self.query_node.getInputPort('time')
        port.writeDouble(value)
        self.dataflow.needProcessInput(self.query_node)

    def dataflowBeforeProcessInput(self, node):
        print('Lab before ProcessingInput')

    def dataflowAfterProcessInput(self, node):
        print('Lab after ProcessingInput')


    def run(self):
        while self.dataflow.dispatchPublishedMessages():
            print('tick')

