from visuslab.simple import Simple
import OpenVisus as ov


if __name__ == '__main__':
    ov.SetCommandLine("__main__")
    ov.IdxModule.attach()
    ov.NodesModule.attach()
    ov.VISUS_REGISTER_NODE_CLASS("visuslab.ViewerNode")

    lab = Simple()
    lab.load("http://atlantis.sci.utah.edu/mod_visus?dataset=david")
    lab.start()

    ov.NodesModule.detach()
    ov.IdxModule.detach()