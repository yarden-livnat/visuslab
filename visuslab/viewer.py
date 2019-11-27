from IPython.display import display
import itk
from itkwidgets import view

import OpenVisus as ov


class ViewerNode(ov.Node):
    def __init__(self):
        super().__init__()
        self.addInputPort("array")
        self.addInputPort("dataset")
        self.view = view()
        self.view.ui_collapsed = True
        self._bounds = None
        self.view.observe(self.camera_changed, ['camera'])

    def getTypeName(self):
        return "ViewerNode"

    def getOsDependentTypeName(self):
        return "ViewerNode"

    def processInput(self):
        print("Viewer: processInput")
        super().processInput()
        self.abortProcessing()

        if self.getInputPort('dataset').hasNewValue():
            self.adjust_camera()

        if self.getInputPort('array').hasNewValue():
            self.new_data()
        return True

    def adjust_camera(self):
        print('Viewer: new dataset')

    def new_data(self):
        print("Viewer:read array")
        data = self.readArray("array")
        print("Viewer: received array")
        if data is None or not data.valid():
            print('invalid data')
            return False

        self.a = ov.Array.toNumPy(data, bSqueeze=True, bShareMem=False)
        print('Viewer: array shape', self.a.shape)
        self.view.image = itk.image_view_from_array(self.a, True)
        return True

    @property
    def bounds(self):
        return self._bounds

    @bounds.setter
    def bounds(self, bounds):
        self._bounds = bounds
        self.camera.guessPosition(bounds.toAxisAlignedBox())
        pos = ov.Point3d()
        dir = ov.Point3d()
        vup = ov.Point3d()
        self.camera.getLookAt(pos, dir, vup)

    def camera_changed(self, change):
        print('camera changed')

    def _ipython_display_(self, **kwargs):
        display(self.view)

