from visuslab.lab import VisusLab
from visuslab.viewer import ViewerNode
from OpenVisus import *


if __name__ == '__main__':
    SetCommandLine("__main__")
    IdxModule.attach()
    # VISUS_REGISTER_NODE_CLASS("visuslab.ViewerNode")

    lab = VisusLab()
    lab.run()

    IdxModule.detach()