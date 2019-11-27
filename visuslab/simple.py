import time
import OpenVisus as ov

from .lab import VisusLab
from .viewer import ViewerNode


class Simple(VisusLab):
    def __init__(self, view_dependent=True):
        super().__init__()
        ov.VISUS_REGISTER_NODE_CLASS("visuslab.ViewerNode")

        self.field = None
        self.bounds = None
        self._data = None
        self._view_dependent = False
        self.camera = ov.OrthoCamera(1.3)

        self.view_dependent = view_dependent

        self.dataset_node = ov.DatasetNode()
        self.dataset_node.setName('Dataset node')
        self.addNode(self.dataset_node)

        self.query_node = ov.QueryNode()
        self.query_node.setVerbose(True)
        self.query_node.setName('query node')
        self.query_node.setAccessIndex(0)
        self.query_node.setProgression(ov.QueryNoProgression)
        self.query_node.setQuality(ov.QueryDefaultQuality)
        self.query_node.setViewDependentEnabled(True)

        self.addNode(self.query_node)
        self.connectNodes(self.dataset_node, "dataset", self.query_node)

        self.viewer_node = ViewerNode()
        self.viewer_node.setName('viewer node')
        self.addNode(self.viewer_node)
        self.connectNodes(self.query_node, "array", self.viewer_node)
        self.connectNodes(self.dataset_node, "dataset", self.viewer_node)

    def load(self, url):
        self._data = ov.LoadDataset(url)
        # self.bounds = self.bounds.scaleAroundCenter(0.01)  # 1% of the overall dataset
        self.dataset_node.setDataset(self._data, True)
        self.bounds = self.dataset_node.getBounds()
        self.query_node.setBounds(ov.Position(self.bounds))
        self.query_node.setQueryBounds(ov.Position(self.bounds))
        ba = self.bounds.toAxisAlignedBox()

        self.camera.guessPosition(ba)
        x2, y2 = self.viewer_node.view.viewport
        f = self.camera.getFinalFrustum(ov.Rectangle2d(0, 0, x2, y2))
        self.query_node.setNodeToScreen(f)
        self.set_time(self._data.getDefaultTime())
        self.set_field_name(self._data.getDefaultField().name)

    @property
    def view_dependent(self):
        return self._view_dependent

    @view_dependent.setter
    def view_dependent(self, v):
        if self._view_dependent != v:
            self._view_dependent = v
            self.update_view()

    def update_view(self):
        print("update_view")
        if self._data is not None:
            if self.view_dependent:
                if False:
                    bounds = self.dataset_node.get_bounds()
                    self.viewer_node.bounds = self.bounds
                else:
                    x1,y1, x2, y2 = self.bounds.p1[0], self.bounds.p1[1], self.bounds.p2[0], self.bounds.p2[1]
                    print('bounds:', x1, x2, y1, y2)
                    frustum = ov.Frustum()
                    frustum.loadModelview(ov.Matrix.identity(4))
                    frustum.loadProjection(ov.Matrix.ortho(x1, x2, y1, y2, -1, +1))
                    frustum.setViewport(ov.Rectangle2d(0, 0, x2 - x1, y2 - y1))
                    self.query_node.setNodeToScreen(frustum)

    def set_field_name(self, name):
        self.query_node.getInputPort('fieldname').writeString(name)
        self.needProcessInput(self.query_node)

    def set_time(self, value):
        port = self.query_node.getInputPort('time')
        port.writeDouble(value)
        self.needProcessInput(self.query_node)

    def processInput(self, node):
        print('lab: processInput')
        super().processInput(node)


