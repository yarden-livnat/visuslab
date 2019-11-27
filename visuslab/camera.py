

class Ortho(object):
    def __init__(self, left=0, right=0, bottom=0, top=0, zNear=0, zFar=0):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.zNear = zNear
        self.zFar = zFar

    def fixAspectRatio(self, old, new):
        if old.width == 0 or new.width == 0:
            return
        if old.width and old.width:
            self.scaleAroundCenter()


class Camera(object):
    def __init__(self):
        self.scale = 1.3
        self.ortho = Ortho()

    def setViewport(self, value):
        self.ortho.fixAspectRatio();

    def guessPosition(self, bounds):
        pass


    def frustum(self):
        pass